import boto3
rek = boto3.client('rekognition')
with open('filename.png', 'rb') as img:
msg = rek.index_faces(
    CollectionId='54321',
    Image={
        # Possibly bytesarray(img)
        'Bytes': img,
    },
    ExternalImageId='string',
    DetectionAttributes=[
        'ALL',
    ]
)
