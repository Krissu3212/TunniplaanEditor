# Find the column's lessons borders with checking for white and black color loops
# Fully self-made, obviously

from PIL import Image
import pytesseract
import cv2
import numpy as np

lessonsLocations = []
def edit():
    # Add the first lessons location to the list, because we already know its location is right at the beginning
    lessonsLocations.append(0)
    
    # Open esm edited image. There's one bug: we need to open the column which is the longest, because according to that column the code will put the lesson times
    mask = Image.open("cropEsmEdited.png")
    maskOpen = mask.load()
    
    # Logic for finding the lesson borders locations
    downY = 1
    print("Tere")
    while downY < mask.size[1] - 10:
        if (maskOpen[5, downY][0] > 0): # 5 so it wouldn't begin from the first pixel
            print("HERE")               # [0], because its a tuple and i need to select one value from it (RGB - value, value, value), and if its black i know every value is 0, and not if the colors not black...
            print(maskOpen[5, downY][0])# ...and i just discovered this method. I think earlier i could have done it too and i could have written much simpler code
            print(downY)
            downY = downY + 1
        elif (maskOpen[5, downY][0] == 0):
            print("black found")
            if (maskOpen[5, downY - 1][0] == 0 and maskOpen[5, downY][0] == 0):
                print("Moving on missing color area")
                downY = downY + 1
            if (maskOpen[5, downY - 1][0] > 0 and maskOpen[5, downY][0] == 0 and maskOpen[5, downY + 1][0] == 0): # == 255
                print("Missing color area begins")
                lessonsLocations.append(downY)
                print(lessonsLocations)
                downY = downY + 1
            elif (maskOpen[5, downY - 1][0] > 0 and maskOpen[5, downY][0] == 0 and maskOpen[5, downY + 1][0] > 0): # == 255
                print("Border found")
                lessonsLocations.append(downY)
                print(lessonsLocations)
                downY = downY + 1
            elif (maskOpen[5, downY - 1][0] == 0 and maskOpen[5, downY][0] == 0 and maskOpen[5, downY + 1][0] > 0): # == 255
                print("Missing color area ends")
                lessonsLocations.append(downY)
                downY = downY + 1
    print(lessonsLocations)            



                
                



    
