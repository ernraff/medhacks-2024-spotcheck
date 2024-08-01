import json
import boto3

bucket = "lesionimagebucket";

def getRecommendation(fileName):
    # Get classification from image metadata based on filename
    client = boto3.client('s3')
    classification = None
    recommendation = "None"
    
    try: 
        response = client.head_object(Bucket = bucket,  Key = fileName)
        classification = response["ResponseMetadata"]["HTTPHeaders"].get("x-amz-meta-classification", "")
        
        # print("Show me HTTPHeaders: ", response["ResponseMetadata"]["HTTPHeaders"])
        # print("show me response metadata: ", response["ResponseMetadata"])
        
        if classification: 
            print("classification: ", classification)
            #print appropriate recommendation based on classification
            if classification == "benign": 
                recommendation = "Our analysis suggests that this lesion is likely benign. However, we recommend consulting a dermatologist to confirm and ensure your health and safety."
            else:
                recommendation = "Our analysis suggests that this lesion may require further examination. We strongly recommend consulting a dermatologist for a professional evaluation."
        else: 
            recommendation = "This image is not classified."
            
    except Exception as e: 
        print("Failed to fetch metadata: ", e)
    
    return recommendation
    
    
    
def lambda_handler(event, context):

    
    fileName = event['pathParameters']['fileName']
    recommendation = getRecommendation(fileName)
    
    return {
        'statusCode': 200,
        'body': recommendation
        
    }

