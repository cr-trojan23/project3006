from math import e
import boto3
import cv2
import time
import mysql.connector
import json
import random
import datetime
from colorama import Fore, init, Style
from colorama.initialise import deinit
from botocore.exceptions import ClientError


# For new user registration
def registerFaces(targetCapture):
    s3 = boto3.client("s3")  # S3 client (S3 is an object storage service)
    bucket = "project3006"  # Bucket name (Folder to store images in S3)
    print("[INFO]: Uploading image to S3")
    name = input("Enter your name: ")  # Name of user
    age = input("Enter your age: ")  # Age of user
    start_date = str(datetime.date.today())  # Start date of user
    end_date = input("Enter your end date: ")  # End date of user
    image = name + age + start_date + end_date + ".png"  # Name of image
    ra = random.randint(1, 999)  # Random number
    lic_num = end_date + start_date + age + str(ra)  # License number of user
    try:
        # Upload targetCapture image to project3006 bucket with name someuser1.jpg
        s3.upload_file(targetCapture, bucket, image)
        print("[INFO]: Image uploaded to S3")
        insertRDS(
            name, age, start_date, end_date, image, lic_num
        )  # Insert user details into RDS
    except ClientError as e:  # If error, print error
        print(e)


# For comparing faces
def compareFaces(target):
    # Rekognition client (Rekognition is a service that recognizes faces in images)
    rekognition = boto3.client("rekognition")
    s3 = boto3.client("s3")  # S3 client (S3 is an object storage service)
    print("[INFO]: Connected to Rekognition")
    print("[INFO]: Connected to S3")
    print("[INFO]: Comparing faces")
    similarity = 0.00
    # loop through all the images in the bucket and compare them to the target image
    for image in s3.list_objects(Bucket="project3006")["Contents"]:
        imageSource = {"S3Object": {"Bucket": "project3006", "Name": image["Key"]}}
        imageTarget = open(target, "rb")  # Image of user taken when comparing

        try:
            response = rekognition.compare_faces(
                SimilarityThreshold=98,
                SourceImage=imageSource,
                TargetImage={"Bytes": imageTarget.read()},
            )  # Compare faces

            # print("[INFO]: Faces compared")
            for faceMatch in response["FaceMatches"]:
                similarity = float(faceMatch["Similarity"])
                print(similarity, "s")

            if similarity > 98.5:
                imageTarget.close()  # Close imageTarget
                print("[INFO]: Face matched")
                print("The face is " + str(similarity) + "% similar")
                fetchRDS(image["Key"])
                break
            elif image == s3.list_objects(Bucket="project3006")["Contents"][-1]:
                print(Fore.RED + "[INFO]: Face not matched")
                print("The face is " + str(similarity) + "% similar")
                imageTarget.close()
                break
            else:
                continue

        except ClientError as e:  # On recieving an error, print error
            if e.response["Error"]["Code"] == "InvalidParameterException":
                print(Fore.RED + "Face not found")


# Capture image from webcam
def capture():
    camera = cv2.VideoCapture(0)  # Open webcam
    print("[INFO]: Capturing image")
    print("[INFO]: Press SPACE to capture image or ESC to exit")
    time.sleep(2)  # Wait for 2 seconds
    while True:
        ret, frame = camera.read()  # Read image from webcam
        if not ret:
            print("[INFO]: Failed to capture image.")
        cv2.namedWindow("Capturing", cv2.WINDOW_NORMAL)  # Create window
        cv2.imshow("Capturing", frame)  # Show image
        key = cv2.waitKey(1)  # Wait for key press
        if key % 256 == 27:  # If esc key is pressed, exit
            camera.release()
            cv2.destroyAllWindows()
            print("[INFO]: Esc key pressed, Exiting")
            exit()

        elif key % 256 == 32:  # if space key is pressed, save image
            cv2.imwrite("/tmp/img.png", frame)
            print("[INFO]: Image captured")
            camera.release()
            cv2.destroyAllWindows()
            break


# Insert user details into RDS
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
    cursor = mysql_connection.cursor(buffered=True)
    sql = "SELECT * FROM users where image = %s"
    val = (name,)
    cursor.execute(sql, val)
    row = cursor.fetchone()
    init()
    print(Fore.YELLOW + "Biometric Authentication SUCCESS!!")
    print(Style.RESET_ALL + "[INFO]: Printing data from RDS")
    print(Fore.GREEN + "Name: " + row[0])
    print(Fore.GREEN + "Age: " + str(row[1]))
    print(Fore.GREEN + "Start Date: " + str(row[2]))
    print(Fore.CYAN + "End Date: " + str(row[3]))
    print(Style.RESET_ALL + "[INFO]: Data fetched from RDS, Closing connections")
    deinit()
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
    else:
        print("Invalid choice")
        main()


if __name__ == "__main__":
    main()
