import boto3
import cv2
import time
from botocore.exceptions import ClientError, ProfileNotFound

# For new user registration
def registerFaces(targetCapture):
    s3 = boto3.client("s3")  # S3 client (S3 is an object storage service)
    bucket = "project3006"  # Bucket name (Folder to store images in S3)
    try:
        # Upload targetCapture image to project3006 bucket with name someuser1.jpg
        s3.upload_file(targetCapture, bucket, "someuser1.jpg")
    except ClientError as e:  # If error, print error
        print(e)


# For comparing faces
def compareFaces(target):
    # Rekognition client (Rekognition is a service that recognizes faces in images)
    rekognition = boto3.client("rekognition")
    confidence = ""
    imageSource = {
        "S3Object": {"Bucket": "project3006", "Name": "someuser1.jpg"}
    }  # Image of user taken when registering
    imageTarget = open(target, "rb")  # Image of user taken when comparing

    try:
        response = rekognition.compare_faces(
            SimilarityThreshold=98,
            SourceImage=imageSource,
            TargetImage={"Bytes": imageTarget.read()},
        )  # Compare faces

        if len(response["FaceMatches"]) == 0:
            print("No match found")
        else:
            for faceMatch in response["FaceMatches"]:  # For each face match
                confidence = str(faceMatch["Face"]["Confidence"])
                print(
                    "The face matches with " + confidence + "% confidence"
                )  # Print confidence

    except ClientError as e:  # If error, print error
        if e.response["Error"]["Code"] == "InvalidParameterException":
            print("Face not found")

    imageTarget.close()  # Close imageTarget


# Capture image from webcam
def capture():
    camera = cv2.VideoCapture(0)  # Open webcam
    ret, frame = camera.read()  # Read image from webcam
    time.sleep(2)  # Wait 2 seconds
    cv2.imwrite("/tmp/img.png", frame)  # Save image to /tmp/img.jpg
    camera.release()  # Release webcam


def main():
    print("What do you want to do?\n 1. Register\n 2. Compare\n 3. Exit")
    choice = input()
    if choice == "1":
        capture()  # Capture image from webcam
        targetCapture = "/tmp/img.png"  # Target image
        registerFaces(targetCapture)  # Register image
    elif choice == "2":
        capture()  # Capture image from webcam
        targetCapture = "/tmp/img.png"  # Target image
        compareFaces(targetCapture)  # Compare image
    elif choice == "3":
        exit()


if __name__ == "__main__":
    main()
