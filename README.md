# MedHacks 2024 Melanoma Detection

## Overview

This project is my submission for the MedHacks 2024 Hackathon.

A recent [survey]([url](https://preventcancer.org/article/skin-deep-understanding-skin-cancer-in-darker-tones/#:~:text=The%20Prevent%20Cancer%20Foundation's%202024,had%20a%20skin%20cancer%20check.) by the Prevent Cancer Foundation found that more than half of American adults are not up to date on their annual skin cancer screenings.  This is concerning given that skin cancer is one of the most common types of cancer in the US, with more than 3.3 million Americans affected by non-melanoma skin cancers. 

It is not uncommon to notice small lesions or unusual freckles pop up, but many of us put of seeing a dermatologist.  

The motivation for this project is to aid users in performing routine self-screenings by evaluating skin lesions and recommending further evaluation by a medical professional if indicated.

## Architecture

![medhacks_architecture drawio](https://github.com/user-attachments/assets/7eab6476-a8d4-4b8a-a256-9a3ec552074d)

## Program Flow

1.  Client is authenticated using AWS Cognito
2.  Client uploads photo of skin lesion to S3 bucket
3.  User makes API call to GET method
4.  Lambda proxy triggers AWS Sagemaker
5.  Jupyter notebook preprocesses image from S3 bucket and passes it to pre-trained deep learning model
6.  Model classifies image as BENIGN or MALIGNANT
7.  Lambda proxy returns recommendation for further evaluation to user based on image classification.
  - If the image is classified as benign: Our analysis suggests that this lesion may require further examination. We strongly recommend consulting a dermatologist for a professional evaluation.
  - If the image is classified as benign:  Our analysis suggests that this lesion is likely benign. However, we recommend consulting a dermatologist to confirm and ensure your health and safety.

## Disclaimer 

The results provided by this app are based on a deep learning model and are for informational purposes only. They should not be considered as medical advice, diagnosis, or treatment. Only a licensed healthcare professional can provide accurate medical advice and diagnosis. We strongly recommend consulting a dermatologist or healthcare provider for a professional evaluation, regardless of the app's prediction. By using this app, you acknowledge and agree to these terms and understand that the app is not a substitute for professional medical advice.

## Limitations
1.  Model accuracy:
   - False negatives could result in users not seeking medical attention in a timely manner
   - False positives could result in unnecessary anxiety for the user
2.  Data bias:
  - Training data for AI models comes from a healthcare system that is inherantly biased.
  - Models may be less effective in detecting malignant lesions in patients of color than in their white counterparts.

