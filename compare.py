import boto3
import cv2
import time
from botocore.exceptions import ClientError

def registerFaces(targetCapture):
    s3 = boto3.client('s3')
    bucket = 'project3006'
    try:
        s3.upload_file(targetCapture, bucket, 'someuser1.jpg')
    except ClientError as e:
        print(e)

def compareFaces(target):
    rekognition = boto3.client('rekognition')
    imageSource = {
        'S3Object': {
            'Bucket': 'project3006',
            'Name': 'someuser1.jpg'
        }
    }
    imageTarget = open(target, 'rb')
    response = rekognition.compare_faces(SimilarityThreshold=80,
                                        SourceImage=imageSource,
                                        TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face matches with ' + confidence + '% confidence')
        
    imageTarget.close()


def capture():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    time.sleep(2)
    cv2.imwrite('/tmp/img.jpg', frame)
    camera.release()


def main():
    print("What do you want to do?\n 1. Register\n 2. Compare\n 3. Exit")
    choice = input()
    if choice == '1':
        capture()
        targetCapture = '/tmp/img.jpg'
        registerFaces(targetCapture)
    elif choice == '2':
        capture()
        targetCapture = '/tmp/img.jpg'
        compareFaces(targetCapture)
    elif choice == '3':
        exit()


if __name__ == '__main__':
    main()
