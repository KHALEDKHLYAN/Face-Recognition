import tkinter as tk
from tkinter import Message, Text
import cv2, os
import csv
import numpy as np
from PIL import Image, ImageTk
import tkinter.font as font
# The code imports the necessary modules, including the tkinter module, OpenCV (cv2), and PIL (Python Imaging Library) modules.

window = tk.Tk()
window.title("KGCE BE-IT 2020")
window.configure(background='black')
window.geometry('1280x670')
# The code initializes a tkinter window with a black background, a title of "KGCE BE-IT 2020," and a geometry of 1280x670.

lbl = tk.Label(window, text="Face Recognition Based Attendance System", bg="white" , fg="black" , width=50 , height=3, font=('times', 30, 'italic bold')) 
lbl.place(x=100, y=20)
# The code initializes a tkinter window with a black background, a title of "KGCE BE-IT 2020," and a geometry of 1280x670.

lbl1 = tk.Label(window, text="Enter ID", width=20 , height=2 , fg="black" , bg="white", font=('times', 15, ' bold ') ) 
lbl1.place(x=200, y=200)
# The code creates a label widget with the text "Face Recognition Based Attendance System," a white background, and a font of Times New Roman, size 30 with an italic bold effect. 
# The widget is placed at the x and y coordinates (100, 20) in the window

txt1 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 15, ' bold '))
txt1.place(x=550, y=215)
# The code creates a label widget with the text "Enter ID," a white background, a font of Times New Roman, size 15, and bold. The widget is placed at the x and y coordinates (200, 200) in the window.


lbl2 = tk.Label(window, text="Enter Name", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 15, ' bold ')  )
txt2.place(x=550, y=315)

lbl3 = tk.Label(window, text="Notification →", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
lbl3.place(x=200, y=400)

message = tk.Label(window, text="", bg="white", fg="black", width=30, height=2, font=('times', 15, ' bold ')) 
message.place(x=550, y=400)
 
def clearId():
    txt1.delete(0, 'end')

def clearName():
    txt2.delete(0, 'end')

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

# This function captures images using the device's camera and saves them along with the user's ID and name
def takeImages():        
    Id=(txt1.get())
    name=(txt2.get())
# Check if ID is numeric and name is alphabetical
if(isNumber(Id) and name.isalpha()):
    
    # Open camera to capture images
    cam = cv2.VideoCapture(0)
    
    # Load haarcascade for face detection
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector=cv2.CascadeClassifier(harcascadePath)
    
    # Initialize sample number to 0
    sampleNum=0
    
    # Keep capturing images until user presses 'q' or 60 images are taken
    while(True):
        # Capture image from camera
        ret, img = cam.read()
        
        # Convert image to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the image using the loaded haarcascade
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        # Draw a rectangle around the detected face and save the image in the SampleImages folder
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
            sampleNum=sampleNum+1
            cv2.imwrite("SampleImages\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
            
            # Display the image with the rectangle around the face
            cv2.imshow('Face Detecting',img)
        
        # Break the loop if the user presses 'q'
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        
        # Break the loop if 60 images have been captured
        elif sampleNum>60:
            break
    
    # Release camera and destroy all windows
    cam.release()
    cv2.destroyAllWindows() 
    
    # Add ID and name to StudentRecord.csv file
    res = "Images Saved for ID : " + Id +" Name : "+ name
    row = [Id , name]
    with open('StudentRecord.csv','a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    
    # Display success message in GUI
    message.configure(text= res)

# If ID or name is not in the correct format, display error message in GUI
# If the name entered by the user contains numbers, display an error message
if(isNumber(name)):
    res = "Enter Alphabetical Name"
    message.configure(text= res)

# If the Id entered by the user contains alphabets, display an error message
if(Id.isalpha()):
    res = "Enter Numeric Id"
    message.configure(text= res)


# Function to train the images and create a LBPH face recognizer
def trainImages():
    # Create a recognizer object using LBPHFaceRecognizer
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)

    # Get images and corresponding Ids from the given path
    faces,Id = getImagesAndLabels("SampleImages")

    # Train the recognizer using the faces and corresponding Ids
    recognizer.train(faces, np.array(Id))

    # Save the trained recognizer to a file
    recognizer.save("DataSet\Trainner.yml")
    res = "Image Trained"
    message.configure(text= res)

# Function to get images and corresponding Ids from a given path
def getImagesAndLabels(path):
    # Get the file paths of all the images in the given path
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        # Convert the image to grayscale and convert to numpy array
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')

        # Get the Id of the image from the file name
        Id=int(os.path.split(imagePath)[-1].split(".")[1])

        # Add the image and Id to the respective lists
        faces.append(imageNp)
        Ids.append(Id)        

    # Return the list of faces and corresponding Ids
    return faces,Ids

  
clearButton1 = tk.Button(window, text="Clear", command=clearId, fg="black", bg="white", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
clearButton1.place(x=850, y=200)

clearButton2 = tk.Button(window, text="Clear", command=clearName, fg="black", bg="white", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
clearButton2.place(x=850, y=300)  

takeImg = tk.Button(window, text="Take Images", command=takeImages, fg="black", bg="white", width=20, height=3, activebackground = "Green", font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)

trainImg = tk.Button(window, text="Train Images", command=trainImages, fg="black", bg="white", width=20, height=3, activebackground = "Green" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="black", bg="white", width=20, height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=800, y=500)

lbl4 = tk.Label(window, text="DESIGN BY KGCE BE-IT BATCH 2020, GROUP NO : 10", width=80, fg="white", bg="black", font=('times', 15, ' bold')) 
lbl4.place(x=200, y=620)

window.mainloop()
