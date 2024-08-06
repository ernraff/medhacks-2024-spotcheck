import boto3
import json

# Initialize clients
s3_client = boto3.client('s3')
sagemaker_client = boto3.client('sagemaker-runtime')
s3 = boto3.client('s3')
endpoint_name = 'huggingface-pytorch-inference-2024-08-05-04-22-18-327'

def update_s3_object_metadata(bucket_name, object_key, new_metadata):
    # Retrieve the existing object to get the current metadata
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        existing_metadata = response.get('Metadata', {})
        
        # Update the existing metadata with the new metadata
        existing_metadata.update(new_metadata)

        # Copy the object to itself with the updated metadata
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': object_key},
            Key=object_key,
            Metadata=existing_metadata,
            MetadataDirective='REPLACE'
        )
        print(f"Metadata updated successfully for {object_key}.")
    except Exception as e:
        print(f"Error updating metadata: {e}")

def get_classification(bucket_name, image_key):
    # Download the image from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response['Body'].read()
    except Exception as e:
        print(f"Error downloading image from S3: {e}")
        return None
    
    # Invoke the SageMaker endpoint with raw image data
    try:
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='image/x-image',  # Specifies raw image data
            Accept='application/json',
            Body=image_data  # Raw image data
        )
        result = response['Body'].read().decode()
    except Exception as e:
        print(f"Error invoking SageMaker endpoint: {e}")
        return None

    # Parse the response and find the most likely label
    try:
        predictions = json.loads(result)  # Parse JSON response
        most_likely = max(predictions, key=lambda x: x['score'])  # Find the label with the highest score
        most_likely_label = most_likely['label']
        
        # Determine if the label is benign or malignant
        if most_likely_label in ["melanocytic_Nevi", "benign_keratosis-like_lesions"]:
            return "benign"
        else:
            return "malignant"
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

def lambda_handler(event, context):
    # Define S3 bucket and image key from the event 
    bucket_name =  event['Records'][0]['s3']['bucket']['name']
    image_key =  event['Records'][0]['s3']['object']['key']

    # Get classification
    classification = get_classification(bucket_name, image_key)
    
    if classification:
        # Update metadata if classification is successfully determined
        new_metadata = {'classification': classification}
        update_s3_object_metadata(bucket_name, image_key, new_metadata)
        
        return {
            'statusCode': 200,
            'body': classification
        }
    else:
        return {
            'statusCode': 500,
            'body': "Error determining classification"
        }
