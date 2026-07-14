import cv2
import random
import numpy as np
"""img = cv2.imread("motion tracking project/cat.jpg",cv2.IMREAD_COLOR)
print(img.shape)
print(img[0,0])
grey_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Grey Cat" , grey_img)
cv2.imshow("Cat" , img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
videos=[]
video1=cv2.VideoCapture(1)
video2=cv2.VideoCapture(0)

def generate_image():
    sucess,img =video2.read()
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return sucess,img,gray_img
def save_as_video(frames,i):
    
    #video_name="video:"+str(i)+".avi" #assigns tag to video based on 
    #iteration it was generated to prevent clone videos being saved
    #height,width,layer=frames[0].shape
    #video = cv2.VideoWriter(video_name, 0, 10,(width,height))
    video=[]
    for frame in frames:
        video.append(frame)
    #cv2.destroyAllWindows()
    #video.release()
    return video
def record():
    sensetivity=20 #lower number is more sensetive
    i=0
    movement=False
    frames_since_movement=0
    while True:

        sucess,img,gray_img=generate_image()
        if sucess:
            cv2.imshow("camera",img)
            cv2.imshow("gray",gray_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        if i!=0: #ignore first pass where past_img has no value
            diff= cv2.absdiff(gray_img,past_img)
            thresh = cv2.threshold(diff,sensetivity,225,cv2.THRESH_BINARY)
            
            if cv2.countNonZero(thresh[1]) !=0:
                movement=True
            else:
                movement=False

            if past_movement==False and movement==True:
                frames_since_movement=0
                print("movement started")
                frames=[img]
            elif past_movement==True and movement==True:
                frames_since_movement=0
                frames.append(img)
            elif past_movement==True and movement==False:
                video=save_as_video(frames,i)
                if len(video)>30:

                    videos.append(video)
                print("movement ended")
        #sets current velues to past values to be read next iteration
        past_movement=movement
        past_img=gray_img
        i+=1

        

        
    cv2.destroyAllWindows()
    menu()
def menu():
    choice=input("What would you like to do?\n" \
    "record footage: press 1\n" \
    "watch footage:  press 2\n")
   
 
    if choice=="1":
       record()
    elif choice=="2":
       watch()
   
    else:
       print("invalid")
       menu()
def watch():
    choice = int(input(f"there are {len(videos)} videos saved, which one would you like to watch\n"))-1  
    for i in range(len(videos[choice])):
        cv2.imshow("display",videos[choice][i])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if i==len(videos[choice])-1:
            cv2.destroyAllWindows()
            
            
    menu()
menu()