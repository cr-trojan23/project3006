import boto3
import cv2
import time
import mysql.connector
import json
import random
from botocore.exceptions import ClientError


# For new user registration
def registerFaces(targetCapture):
    s3 = boto3.client("s3")  # S3 client (S3 is an object storage service)
    bucket = "project3006"  # Bucket name (Folder to store images in S3)
    print("[INFO]: Uploading image to S3")
    name = input("Enter your name: ")  # Name of user
    age = input("Enter your age: ")  # Age of user
    start_date = input("Enter your start date: ")  # Start date of user
    end_date = input("Enter your end date: ")  # End date of user
    image = name + age + start_date + end_date + ".png"  # Name of image
    ra = random.randint(1, 100)  # Random number
    lic_num = end_date + start_date + age + str(ra)  # License number of user
    try:
        # Upload targetCapture image to project3006 bucket with name someuser1.jpg
        s3.upload_file(targetCapture, bucket, image)
        print("[INFO]: Image uploaded to S3")
        insertRDS(name, age, start_date, end_date, image, lic_num)
    except ClientError as e:  # If error, print error
        print(e)


# For comparing faces
def compareFaces(target):
    # Rekognition client (Rekognition is a service that recognizes faces in images)
    rekognition = boto3.client("rekognition")
    print("[INFO]: Connected to Rekognition")
    similarity = ""
    imageSource = {
        "S3Object": {"Bucket": "project3006", "Name": "someuser1.jpg"}
    }  # Image of user taken when registering

    print("[INFO]: Fetched image from S3")
    imageTarget = open(target, "rb")  # Image of user taken when comparing

    try:
        print("[INFO]: Comparing faces")
        response = rekognition.compare_faces(
            SimilarityThreshold=98,
            SourceImage=imageSource,
            TargetImage={"Bytes": imageTarget.read()},
        )  # Compare faces

        print("[INFO]: Faces compared")

        for faceMatch in response["FaceMatches"]:  # For each face match
            # Get similarity of match
            similarity = str(faceMatch["Similarity"])

        print("The face is " + similarity + "% similar")  # Print similarity %

    except ClientError as e:  # If error, print error
        print(e.response["Error"]["Message"])
        print("Error: Could not compare faces")

    imageTarget.close()  # Close imageTarget


# Capture image from webcam
def capture():
    camera = cv2.VideoCapture(0)  # Open webcam
    print("[INFO]: Capturing image")
    ret, frame = camera.read()  # Read image from webcam
    time.sleep(2)  # Wait 2 seconds
    cv2.imwrite("/tmp/img.png", frame)  # Save image to /tmp/img.jpg
    print("[INFO]: Image captured")
    camera.release()  # Release webcam


def insertRDS(name, age, start_date, end_date, image, lic_num):
    # MySQL Config
    with open("config.json") as config_file:
        config = json.load(config_file)
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["passwd"]
        database = config["mysql"]["db"]
    mysql_connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    print("[INFO]: Connected to RDS")
    cursor = mysql_connection.cursor()
    sql = "INSERT INTO users (name, age, start_date, end_date, image, lic_num) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name, age, start_date, end_date, image, lic_num)
    cursor.execute(sql, val)
    mysql_connection.commit()
    print("[INFO]: Data uploaded to RDS")
    cursor.close()
    mysql_connection.close()


def fetchRDS(name):
    # MySQL Config
    with open("config.json") as config_file:
        config = json.load(config_file)
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["passwd"]
        database = config["mysql"]["db"]
    mysql_connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    print("[INFO]: Connected to RDS")
    cursor = mysql_connection.cursor()
    sql = "SELECT * FROM users where name = %s".format(name)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    mysql_connection.close()


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
