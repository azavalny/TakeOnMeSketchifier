import cv2
from ImageSketcher import ImageSketcher
import numpy as np
import moviepy as mp


def main():
    print("\nWelcome to the Take-On-Me Multi-Input-Converter\nYou can choose as your input to be either a:")
    print("i (for Image)\nv (for Live Webcam)\n")

    response = input("First, Select an Input type:")

    if response.lower() in ["i","image","pic","picture"]:
        print("\nNext, you'll need to put the image file in same the folder with everything else")

        #makes sure that the image file exists
        while True:
            name = input("Enter the file name of your image (include file extension like .png,.jpg):")
            img = cv2.imread(name)
            if img is not None:
                break

        response2 = input("\nYour image is now ready to process\nDo you want to resize your ouput? y/n :")
        
        if response2.lower() in ["y","yes"]:
            OUT_Height = int(input("\nFirst, Enter the height of your new image:"))
            OUT_Width = int(input("\nNext, Enter the width:"))

            img_resized = cv2.resize(img,(OUT_Width,OUT_Height))
            IS = ImageSketcher(img_resized)
            IS.sketch()
            IS.exportImage(name)

            print("\nImage Processed! Go to the folder with these files to view it!")
        else:
            IS = ImageSketcher(img)
            IS.sketch()
            IS.exportImage(name)
            print("\nImage Processed! Go to the folder with these files to view it!")

    else:
        webcam = cv2.VideoCapture(0)
        while True:
            ret, frame = webcam.read()
            IS = ImageSketcher(frame)
            IS.sketch()
            imgf = np.array(IS.getImg())
            cv2.imshow('Take On Me Live Capture',imgf)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        webcam.release()
        cv2.destroyAllWindows()

while True:
    main()
    ask = input("Would you like to process another image/video/webcam capture? y/n: ")
    if ask.lower() in["n","no"]:
        break
