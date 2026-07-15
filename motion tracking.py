import cv2
import random
import numpy as np
from time import sleep
import keyboard
import tkinter as tk
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
password="hello world"
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
def record(menu_int):
    menu_int.destroy()
    recording=False # chackes if usable recordings are being created
    sensetivity=40 #lower number is more sensetive
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


    menu_int=tk.Tk()
    menu_int.geometry("300x300")
    button1=tk.Button(menu_int,text="Record",width=25,command=lambda:record(menu_int))
    button2=tk.Button(menu_int,text="Watch",width=25,command=lambda:watch(menu_int))
    button3=tk.Button(menu_int,text="Test",width=25,command=lambda:check_camera(menu_int))

    button1.pack()
    button2.pack()
    button3.pack()
    menu_int.mainloop()
    
   
 
    
def watch(menu_int):
    menu_int.destroy()
    choice = int(input(f"there are {len(videos)} videos saved, which one would you like to watch\n"))-1
    if choice==-1:
        menu() #goes straight to menu if user enters 0
        return
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
def check_camera(menu_int):
    menu_int.destroy()
    while True:
        sucess,img,gray_img=generate_image()
        if sucess:
                cv2.imshow("camera",img)       
                cv2.imshow("gray",gray_img)   
        if cv2.waitKey(1) & keyboard.is_pressed('esc'): #still used this method because i know it works for closing image windows but changed to using keyboard to make it coherent with the rest of the code
                cv2.destroyAllWindows()
                menu()
                break

def password_entry():
    def check_password():
        current=entry1.get()
        
        print("checking password")
        print(current)
        if current==password:
            root.destroy()

            menu()
            
    root=tk.Tk()
    root.geometry("400x300")

    
    label1=tk.Label(root,text="enter password")
    
    entry1=tk.Entry(root)
    button1=tk.Button(root,text="enter",width=25,command=lambda:check_password())

    #root.bind("<key>",check_password)

    label1.pack()
    entry1.pack()
    button1.pack()
    
    root.mainloop()
password_entry()
