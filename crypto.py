from os import lstat
import numpy as np
import imageio
from PIL import Image as im
from numpy.core.records import array
import matplotlib.pyplot as plt

def fibshift(st):
    fibarr=[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811]
    n=len(st)
    s1=""
    for i in range(n):
        b=ord(st[i])%len(fibarr)
        ind=(2**fibarr[b])%n
        s1+=st[ind]
    return s1


def doubler(st):
    n=len(st)
    s=""
    for i in range(n):
        s+=st[i*(2**i)%n]
    return s



def func(st):
    n=len(st)
    s=""
    #y=7*(x**4)+6*(x**2)+3*(x**3)+121*x+1231--equation
    for i in range(n):
        x=ord(st[i])
        y=7*(x**4)+6*(x**2)+3*(x**3)+121*x+1231
        b=y%128
        s+=chr(b)
    return s

def box(st):
    box=[[4,0,1,2,3],[1,4,5,0,3,2],[5,1,4,6,0,2,3],[5,0,3,1,2,4,6,7],[6,7,1,3,0,8,2,4,5],[5,7,8,3,2,6,9,0,1,4],[2,5,6,3,9,1,8,4,10,0,7],[9,6,7,2,5,1,4,10,8,0,11,3],[4,6,2,8,9,1,5,7,12,0,10,3,11],[11,2,7,1,3,6,5,9,10,12,0,13,4,8],[12,4,13,7,8,9,1,14,0,2,5,6,3,10,11],[1,4,7,9,0,2,14,12,15,3,5,6,10,11,8,13],[3,15,12,10,5,6,2,1,0,9,8,7,4,11,16,13,14],[6,3,7,9,1,2,0,10,15,16,12,11,4,8,13,5,17,14],[8,5,18,11,15,14,17,2,3,9,7,1,0,10,4,6,13,12,16],[19,1,3,4,7,6,8,2,12,11,5,14,17,0,18,10,13,15,9,16,]]
    a=len(st)-5
    s=""
    arr=box[a]
    for i in range(len(arr)):
        s+=st[arr[i]]
    return s
def nd(st):
    n=len(st)
    s=""
    w=23232
    for i in range(n):
        y=((7*(i+1)^23) +i+21)%n
        s+= chr(ord(st[i]) and ord(st[y]) or not  ord(st[y]))
    return s

def pad(st):
    
    n=len(st)
    s1=""
    s="!a@b#c1$2(d34e5^f&7g*h86j)k_l9+m0=n-o[p\qr]stuv;w:x/y>z<"
    for i in range(n):
        x=ord(st[i])
        b=(x+(i+1)**x)%len(s)
        s1+=s[b]
    return s1
        


acc=input("Enter the account name ")
st=input("Enter the pass of length 5-20 " )
n=len(st)
c=0

#username-->anupam
#abcd->>jasdhfkj
for i in range(n):
    b=(ord(st[i])^ord(acc[i%len(acc)]))
    c+=b

permut_list=["FEBCDA","CEFBDA","BCEFDA","CFEBAD","BAFCDE","ABFCDE","DEBCFA","CABADF","FEDCAB","BDAFCE"]
x=b%50
myroute=permut_list[b%10]*5
#print(myroute)
for i in range(len(myroute)):
    if myroute[i]=="A":
        st=fibshift(st)
    elif myroute[i]=="B":
        st=func(st)
    elif myroute[i]=="C":
        st=nd(st)
    elif myroute[i]=="D":
        st=box(st)
    elif myroute[i]=="E":
        st=doubler(st)
    elif myroute[i]=="F":
        st=pad(st)
    
s=""
iml2=[]
for i  in range(len(st)):
    s+=hex(ord(st[i]))[2:]

for i in range(len(s)):
    iml2.append(ord(s[i]))
#print(st)
#print(iml2,len(iml2))

lst=iml2
n=len(lst)
img=im.open("C:\\Users\\ANUPAM\\Desktop\\images.jpg")


arr=np.asarray(img)
np.uint8(arr)
sh=arr.shape
a,b,c=sh[0],sh[1],sh[2]
bs=np.reshape(arr,(sh[0]*sh[1]*sh[2],))

l1=list(bs)
for i in range(n):
    l1[x+i]=lst[i]

new_res=np.array(l1)

array=np.reshape(l1,(a,b,3))

op=int(input("do you want to sign_in(1) or  create a new account(2):"))


if op==2:
    plt.imshow(array)

    #plt.show()

    #plt.savefig('C:\\Users\\ANUPAM\\Desktop\\crypto\\img1.png')
    plt.close()
    np.uint8(array)
    
    imageio.imwrite("C:\\Users\\ANUPAM\\Desktop\\crypto\\"+acc+".jpg",array)

    print()
    print()
    print("*****************************************************************************************")
    print("Your data has been feeded")
else:
    np.uint8(array)
    imageio.imwrite("C:\\Users\\ANUPAM\\Desktop\\verify\\"+acc+".jpg",array)
    ans=im.open("C:\\Users\\ANUPAM\\Desktop\\crypto\\"+acc+".jpg")
    img1=im.open("C:\\Users\\ANUPAM\\Desktop\\verify\\"+acc+".jpg")
    print()
    print()
    print("******************************************************************************************")
    print(img1==ans,"Password")

