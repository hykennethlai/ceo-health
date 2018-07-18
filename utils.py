import requests
from urllib import request
import pandas as pd
import boto3
import sys
import os
import numpy as np
import time

CREDENTIALS_FILE_NAME = 'credentials.txt'

def read_credentials():
    with open(CREDENTIALS_FILE_NAME) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    # in case there are extra spaces in the credentials file
    content_copy = list(content)
    content = []
    for x in content_copy:
        if len(x) > 0:
            content.append(x)

    credentials = [x.split('=')[1].strip() for x in content]

    return credentials

# store credentials in variables
credentials = read_credentials()
AWS_ACCESS_KEY_ID = credentials[0]
AWS_SECRET_ACCESS_KEY = credentials[1]
BUCKET_NAME = credentials[2]
REGION = credentials[3]
MICROSOFT_SUBSCRIPTION_KEY = credentials[4]
FACE_API_URL = credentials[5]

# microsoft face detection settings
headers = {'Ocp-Apim-Subscription-Key': MICROSOFT_SUBSCRIPTION_KEY}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,blur,exposure,noise'
}

# initialize amazon s3 instance
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)