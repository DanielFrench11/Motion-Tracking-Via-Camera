import cv2
import random
import numpy as np
from time import sleep
import keyboard
"""img = cv2.imread("motion tracking project/cat.jpg",cv2.IMREAD_COLOR)
print(img.shape)
print(img[0,0])
grey_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Grey Cat" , grey_img)
cv2.imshow("Cat" , img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
videos=[]
video1=cv2.VideoCapture(0)
video2=cv2.VideoCapture(1)

fps=video2.get(cv2.CAP_PROP_FPS)
print(fps)
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
    recording=False # chackes if usable recordings are being created
    sensetivity=85 #lower number is more sensetive
    i=0
    movement=False
    frames_since_movement=0
    video=[]
    stop_after_frames=fps*5 # amount of frames with no motion required for recording to stop
    min_video_length=fps*2 + stop_after_frames #2 secods of movement along with 5 seconds of no movement required for recording to stop
    while True:
        if keyboard.is_pressed('esc'):
            break

        sucess,img,gray_img=generate_image()
        if sucess:
            #cv2.imshow("camera",img)       #would show coloured and gray image, only enabled for debugging
            #cv2.imshow("gray",gray_img)
            pass
        #if cv2.waitKey(1) & 0xFF == ord('q'): #only worked when images were shown, now used keyboard module
        
           # break

        
            
        if i!=0: #ignore first pass where past_img has no value
            diff= cv2.absdiff(gray_img,past_img)
            thresh = cv2.threshold(diff,sensetivity,225,cv2.THRESH_BINARY)
            
            if cv2.countNonZero(thresh[1]) !=0:
                movement=True
            else:
                movement=False

            """if past_movement==False and movement==True:
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
                print("movement ended")"""
            
            if movement==True:
                frames_since_movement=0
                if recording==True:
                    #continue recording
                    video.append(img)
                else:
                    #start recording
                    video=[img]
                    recording=True
                    print("started recording")
            else:
                if recording==True:
                    video.append(img) #add frames to video even when there isnt movement to ensure accurate recreation
                    if frames_since_movement>stop_after_frames:
                        recording=False
                        print("recording stopped")
                        if len(video)>=min_video_length:
                            print("recording saved")
                            #saves video if it is long enougth
                            
                            videos.append(video)
                        else:
                            print("recording disscarded: Too short!")
                    else:
                        frames_since_movement+=1
        #sets current velues to past values to be read next iteration
        past_movement=movement
        past_img=gray_img
        i+=1

        

        
    cv2.destroyAllWindows()
    menu()
def menu():
    choice=input("What would you like to do?\n" \
    "record footage: press 1\n" \
    "watch footage:  press 2\n" \
    "check camera:   press 3\n")
   
 
    if choice=="1":
       record()
    elif choice=="2":
       watch()
    elif choice=="3":
        check_camera()
    else:
       print("invalid")
       menu()
def watch():
    choice = int(input(f"there are {len(videos)} videos saved, which one would you like to watch\n"))-1  
    print(f" this video has {len(videos[choice])} frames")
    for i in range(len(videos[choice])):
        cv2.imshow("display",videos[choice][i])
        if cv2.waitKey(1) & keyboard.is_pressed('esc'): #still used this method because i know it works for closing image windows but changed to using keyboard to make it coherent with the rest of the code
            cv2.destroyAllWindows()
            break
        if i==len(videos[choice])-1:
            cv2.destroyAllWindows()
        sleep(1/fps)
    menu()       
def check_camera():
    while True:
        sucess,img,gray_img=generate_image()
        if sucess:
                cv2.imshow("camera",img)       
                cv2.imshow("gray",gray_img)   
        if cv2.waitKey(1) & keyboard.is_pressed('esc'): #still used this method because i know it works for closing image windows but changed to using keyboard to make it coherent with the rest of the code
                cv2.destroyAllWindows()
                menu()
                break
    
menu()
