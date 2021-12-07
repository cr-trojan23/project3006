def hasher(st):
    n=len(st)
    st+=st;

    for i in  range(n):
        s1=ord(st[i])^ord(st[n-i-1])
    s1=s1^ord("X")
    return s1

from datetime import timedelta
from datetime import datetime
from deepface import DeepFace
import cv2, shutil,os
from keras.backend import identity
import mysql.connector as plq
print("Hi welcome to __ bus..lets check weather you belong here")

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "C:\\Users\\ANUPAM\\Desktop\\test\\new_image.png"
        cv2.imwrite(img_name, frame)
        print("Image taken and saved click spacebar again if you did not like the image else press escape ")
        

cam.release()

cv2.destroyAllWindows()
print("\n")
print("*****************************************************")
print("Now lets verify   if you are enrolled in our system")
db=DeepFace.find("C:\\Users\\ANUPAM\\Desktop\\test\\new_image.jpg","C:\\Users\\ANUPAM\\Desktop\\mydb")
print("\n")
st=db.head(1)

df=str(st[['identity']])


l=list(df.split(" "))
l2=l[len(l)-1].split("/")
l2=l2[len(l2)-1]
name=l2[:len(l2)-4]
c=0
if name=="":
    print("You are not part of the database kindly enroll ")
    s=input("would  you like to enroll in the system enter y")
    if s=="y" or s=="Y":
        fname=input("Enter your first name")
        lname=input("Enter your  last name ")
        pas=input("Fix a password")
        email=input("Give us the email")
        print("your photo captured would  be  feeded in the database")
        
        shutil.move("C:\\Users\\ANUPAM\\Desktop\\test\\new_image.jpg","C:\\Users\\ANUPAM\\Desktop\\mydb") 
        os.rename("C:\\Users\\ANUPAM\\Desktop\\mydb\\new_image.jpg","C:\\Users\\ANUPAM\\Desktop\\mydb\\"+fname+".jpg")


        cnx=plq.connect(host="localhost",user="root",password="ram123",database="biometric")

        cursor=cnx.cursor()

        cursor.execute("insert into detail values(%s,%s,%s,%s)",(fname,fname+" "+lname,hasher(pas),email))
        #subs=int(input("how many weeks of subscription do you want/ rate per week 100 Rs"))
        #print(subs*100 ,"ruppes to be paid")
        #d=datetime.now()+timedelta(weeks=subs)
        #cursor.execute("insert into detail values(%s,%s)",(name,d))

        cnx.commit()
    else:
        print("Thankyou for using the system please make may for  the next person")     



else:
    print("Hi ",name.upper(),"You are welcome to the bus service")
    c=int(input("is it correct  1 and 0 "))
    pas=input("please enter your password")

    cnx=plq.connect(host="localhost",user="root",password="ram123",database="biometric")

    cursor=cnx.cursor()
    st="select password from detail where custimg='{}'".format(str(name))
    cursor.execute(st)
    
    result=cursor.fetchone()
    #print(result[0],hasher(pas))
    if int(result[0])==hasher(pas):
        print("password matched get inside please")
    else:
        print("Pass word not mathced")
        


cnx=plq.connect(host="localhost",user="root",password="ram123",database="biometric")
cursor=cnx.cursor()
if c==1:
    cursor.execute("update pass set suces=suces+1" )
    cnx.commit()
else:
    cursor.execute("update pass set fail=fail+1" )
    cnx.commit()

os.remove("C:\\Users\\ANUPAM\\Desktop\\mydb\\representations_vgg_face.pkl")