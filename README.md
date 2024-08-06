# SpotCheck Skin Cancer Self-Screener

## Overview

This project is my submission for the MedHacks 2024 Hackathon.

A recent survey by the [Prevent Cancer Foundation](https://preventcancer.org/article/skin-deep-understanding-skin-cancer-in-darker-tones/#:~:text=The%20Prevent%20Cancer%20Foundation's%202024,had%20a%20skin%20cancer%20check.) found that more than half of American adults are not up to date on their annual skin cancer screenings.  This is concerning given that skin cancer is one of the most common types of cancer in the US, with more than 3.3 million Americans affected by non-melanoma skin cancers. 

It is not uncommon to notice small lesions or unusual freckles pop up on our bodies, but many of us put off seeing a dermatologist.  

The motivation for this project is to aid users in performing routine self-screenings by evaluating skin lesions and recommending further evaluation by a medical professional if indicated.

## Architecture

This project utilizes AWS cloud services.  A pre-trained deep learning model for skin cancer detection from [Hugging Face](https://huggingface.co/Anwarkh1/Skin_Cancer-Image_Classification) was used for image classification.

![medhacks_architecture drawio](https://github.com/user-attachments/assets/9cfe2565-6b82-4413-bae1-7dc6dfc0cd69)

## Program Flow

1.  Client uploads photo of skin lesion to S3 bucket, which triggers classifierLambda
2.  classifierLambda passes image to pre-trained model deployed on Sagemaker and classifies image as BENIGN or MALIGNANT
3.  Lambda function adds classification to S3 object's metadata.
4.  Client calls API GET method(/detect/{fileName})
5.  Lambda proxy (getRecommentdation) gets classification label from object metadata and returns recommendation to the user.
    - If the image is classified as malignant: "Our analysis suggests that this lesion may require further examination. We strongly recommend consulting a dermatologist for a professional evaluation."
    - If the image is classified as benign:  "Our analysis suggests that this lesion is likely benign. However, we recommend consulting a dermatologist to confirm and ensure your health and safety."

## Disclaimer 

The results provided by this app are based on a deep learning model and are for informational purposes only. They should not be considered as medical advice, diagnosis, or treatment. Only a licensed healthcare professional can provide accurate medical advice and diagnosis. We strongly recommend consulting a dermatologist or healthcare provider for a professional evaluation, regardless of the app's prediction. By using this app, you acknowledge and agree to these terms and understand that the app is not a substitute for professional medical advice.

## Limitations
1.  Model accuracy:
       - False negatives could result in users not seeking medical attention in a timely manner
       - False positives could result in unnecessary anxiety for the user
2.  Data bias:
      - Training data for AI models comes from a healthcare system that is inherantly biased.
      - Models may be less effective in detecting malignant lesions in patients of color than in their white counterparts.

## Future Work

Due to time constraints, I have focused on the backend of this application for submission.  Next steps will involve building a reactive UI.  

For the sake of expediency I used a pre-trained model for image classifications.  Further training and testing could be done in order to optimize model performance and ensure that recommendations are as accurate as possible.

