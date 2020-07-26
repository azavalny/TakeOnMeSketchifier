import cv2
import scipy.ndimage
import numpy as np
from PIL import Image

thresh_in = 240
thresh_out = 255

#An ImageSketcher takes in an input image and can ouput a sketched version of it
class ImageSketcher():
    def __init__(self,img):
        self.img = img

    def getImg(self):
        return self.img
    #Changes the ImageSketcher's input image into a sketched version
    def sketch(self):
        # Convert into grayscale
        gray = self.grayscale(self.img)

        #Inverting the Image
        gray_INV = 255-gray

        #Blurring the Inverted Image with a Gaussian Filter by a certain sigma factor (a greater sigma->a greater blurring --> greater runtime)
        gray_INV_BLUR = scipy.ndimage.filters.gaussian_filter(gray_INV,sigma=10)

        #Applying a Color Dodge between the blurred inverted and original grayscale image
        #And then returning that as the final image
        imgf = self.dodge(gray_INV_BLUR,gray)

        #Getting the edges of the original grayscale image and then inverting them
        edges = cv2.Canny(self.img,200,300) #TODO Change parameters for lower res images < 500 x 500

        edges_DILATED = cv2.dilate(edges, np.ones((2,2),np.uint8), iterations = 1)

        edges_INV = 255-edges_DILATED

        #Blurring the edges so they're not as sharp
        edges_INV = cv2.GaussianBlur(edges_INV,(3,3),0)

        #Applies a bitwise operator so the edges can subtract from the image and overlay
        imgf = cv2.bitwise_and(imgf,edges_INV,edges_INV)
        
        #Image is thresholded to make the lines appear more distinct
        thresh, imgf = cv2.threshold(imgf, thresh_in, thresh_out, cv2.THRESH_BINARY)

        #Image is then converted to more vibrant gray to accentuate the shading
        imgf = cv2.cvtColor(imgf, cv2.COLOR_GRAY2RGBA)

        #Finally, we convert our image from a 2D array back into an Image object to be exported
        self.img = Image.fromarray(imgf.astype(np.uint8))
        

    #Exports the sketched image to the same directory where this file is located
    def exportImage(self, s):
        self.img = self.img.save(s[:-4] + '_sketched.png')

    #Returns a dodged front and back image
    def dodge(self, front,back): 
        result=front*255/(254-back)  
        result[result>255]=255 
        result[back==255]=255 
        return result.astype('uint8')

    #Returns a grayscale
    def grayscale(self, rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])