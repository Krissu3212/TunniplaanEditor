# YT videos that helped: https://www.youtube.com/watch?v=6DjFscX4I_c&list=PLO_IjgwpIjOt7WFIaJzrK3ATH8uq9hNVv&index=29&t=997s
# Note: cv2 shows 'has no member' errors for me, but the code works
# If you want to change the source image, change the IMAGENAME variable

# Code weakpoints:
# - when code doesn't find "Esm"
# - when code seacrhes for first color and the first lesson's color can be gray which isn't recognized as color to the code
# - when code does the same thing as described above, but then it's checking for the color from below

from PIL import Image
import pytesseract
from cv2 import *
import numpy as np

# Original (source) image
IMAGENAME = "tunniplaan3.png"
IMAGE = Image.open(IMAGENAME)

# Change the gray 1 pixel borders between lessons to white
replaceGrayLines = IMAGE
color_to_find1 = (128, 128, 128, 255)
color_to_replace1 = (255, 255, 255, 255)
new_image_data = []

for color in list(replaceGrayLines.getdata()):
    if (color == color_to_find1):
        new_image_data += [color_to_replace1]
    else:
        new_image_data += [color]
replaceGrayLines.putdata(new_image_data)

# Crop the image with edited gray lines
replaceGrayLinesSize = replaceGrayLines.size
sectionOfImg = replaceGrayLines.crop((0, 0, replaceGrayLinesSize[0], 200))
sectionOfImg.save("sectionOfImg.png")

# Here starts the code to find the location of "Esmaspäev" and other things that come after that
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\krist\AppData\Local\Tesseract-OCR\tesseract.exe'
img = cv2.imread("sectionOfImg.png")
cv2.imshow("sectionOfImg.png", img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

hImg, wImg, _ = img.shape
boxes = pytesseract.image_to_boxes(img)
E = ""
S = ""
for b in boxes.splitlines():
        
    b = b.split(" ")
    print(b)
    # Put red boxes over all letters loop
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4]) 
    cv2.rectangle(img, (x, hImg-y), (w, hImg-h), (0, 0, 255), 1)

    # Check if b[0] is "E", and save the result, then check if b[0] is "s", and if there's also "m", then it has found the "Esm"
    if(b[0] == "E"):
        E = "E"
        eData = b
    if (b[0] == "s" and E == "E"):
            S = "s"
    if (b[0] == "m" and E == "E" and S == "s"):
        print("'Esmaspäev' found")
        E = ""
        S = ""
        # Put a blue triangle over "Esm"
        cv2.rectangle(img, (w - 70, hImg-y + 10), (w + 10, hImg-h - 20), (255, 0, 0), 2)
        # Get the location of "E"
        xPxl, yPxl = eData[1], eData[2]
        print(xPxl, yPxl)
        pxlData = int(xPxl), int(yPxl)
        print(pxlData)

        # Get non-white and non-black colors (Create the black and white image)
        colorImg = cv2.imread("sectionOfImg.png")
        hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

        lower = np.array([0, 5, 20])
        upper = np.array([180, 255, 255])
        
        mask = cv2.inRange(hsv, lower, upper)
        cv2.imshow("Mask", mask) # Show mask (black and white picture) and save it
        cv2.imwrite("mask.png", mask)
        cv2.imshow("Boxes", img) # Show image with original colors, but with removed gray borders
        
        # Re-calculate some cv2 and PIL coordinate differences in the if statement and move downwards by 5 pixels until a color (white) is found on the masked image
        maskOpen = Image.open("mask.png")
        mask = maskOpen.load()  
        maskSize = maskOpen.size
        i = 0
        addY = 5
        
        while (i < 10):
            i = i + 1
            if (mask[pxlData[0], maskSize[1] - pxlData[1] + addY] == 255):
                print("First color found at " + str(pxlData[0]) + ", " + str(maskSize[1] - pxlData[1] + addY)) 
                
                # Check's if there's also a color after 3x5 pixels, starting from the first color's location coordinates
                if (mask[pxlData[0], maskSize[1] - pxlData[1] + addY + 5] == 255):
                    if (mask[pxlData[0], maskSize[1] - pxlData[1] + addY + 10] == 255):
                        if (mask[pxlData[0], maskSize[1] - pxlData[1] + addY + 15] == 255):                
                            # Variable that stores the first found color's location. Needed later in dayColumnsEditor.py cropTheDayNames function.
                            firstColorLocation = pxlData[0], maskSize[1] - pxlData[1] + addY
                            colorCnfrmdCrds = pxlData[0], maskSize[1] - pxlData[1] + addY + 3
                            print("Continuous color confirmed at " + str(colorCnfrmdCrds))
                            
                            # Find the edge (right and left) coordinates of that color
                            subtractX = 0
                            while subtractX < 400:
                                value = mask[pxlData[0] - subtractX, maskSize[1] - pxlData[1] + addY + 3] # + 3 to move down from the egde a little bit
                                if (value == 255):
                                    subtractX = subtractX + 1
                                    #print("Proceeding to move to the side by 1 px.")
                                elif (value == 0):
                                    print("Esm column Left side border found at " + str(pxlData[0] - subtractX), str(maskSize[1] - pxlData[1] + addY + 3))  
                                    EsmLeftBorderX = pxlData[0] - subtractX 
                                    leftBorderY = maskSize[1] - pxlData[1] + addY + 3
                                    

                                    addX = 1
                                    while addX < 400:
                                        value2 = mask[pxlData[0] + addX, maskSize[1] - pxlData[1] + addY + 3]
                                        
                                        if (value2 == 255):
                                            addX = addX + 1
                                            #print("Proceeding to move to the side by 1 px.")
                                        elif (value2 == 0):
                                            print("'Esm' Right side border found at " + str(pxlData[0] + addX), str(maskSize[1] - pxlData[1] + addY + 3))
                                            EsmRightBorderX = pxlData[0] + addX + 1 # Plus one makes it to select the gray one-pixel column on the right side too
                                            EsmRightBorderY = maskSize[1] - pxlData[1] + addY + 3
                                            
                                            # Find the borders of other days columns by just increasing the X axis number and detecting the black color which is the border between columns (just loops inside loops that look for color white - a big mess)
                                            TeiX = 1
                                            while (TeiX < 300):
                                                
                                                if (mask[EsmRightBorderX + TeiX, EsmRightBorderY] == 255):
                                                    TeiX = TeiX + 1
                                                    print("Tei white")
                                                    
                                                elif (mask[EsmRightBorderX + TeiX, EsmRightBorderY] == 0):
                                                    TeiBorderX = EsmRightBorderX + TeiX + 1
                                                    print("Tei border found at x: " + str(TeiBorderX))
                                        
                                                    # Add one because if it was zero it would detect the Tei border
                                                    KolX = 1
                                                    while (KolX < 300):
                                                        if (mask[TeiBorderX + KolX, EsmRightBorderY] == 255):
                                                            KolX = KolX + 1
                                                            print("Kol white")
                                                        elif (mask[TeiBorderX + KolX, EsmRightBorderY] == 0):
                                                            # Here add one to select the gray pixel column
                                                            KolBorderX = TeiBorderX + KolX + 1
                                                            print("Kol border found at x: " + str(KolBorderX))
                                                            
                                                            NelX = 1
                                                            while (NelX < 300):
                                                                if (mask[TeiBorderX + KolX + NelX, EsmRightBorderY] == 255):
                                                                    NelX = NelX + 1
                                                                    print("Nel white")
                                                                elif (mask[TeiBorderX + KolX + NelX, EsmRightBorderY] == 0):
                                                                    NelBorderX = TeiBorderX + KolX + NelX + 1
                                                                    print("Nel border found at x: " + str(NelBorderX))
                                                                    
                                                                    ReeX = 1
                                                                    while (ReeX < 300):
                                                                        if (mask[TeiBorderX + KolX + NelX + ReeX, EsmRightBorderY] == 255):
                                                                            ReeX = ReeX + 1
                                                                            print("Ree white")
                                                                        elif (mask[TeiBorderX + KolX + NelX + ReeX, EsmRightBorderY] == 0):
                                                                            ReeBorderX = TeiBorderX + KolX + NelX + ReeX + 1
                                                                            print("Ree border found at x: " + str(ReeBorderX))
                                                                        
                                                                            crop = IMAGE
                                                                            cropEsm = crop.crop((EsmLeftBorderX, 0, EsmRightBorderX, crop.size[1]))
                                                                            cropTei = crop.crop((EsmRightBorderX - 1, 0, TeiBorderX, crop.size[1]))
                                                                            cropKol = crop.crop((TeiBorderX - 1, 0, KolBorderX, crop.size[1]))
                                                                            cropNel = crop.crop((KolBorderX - 1, 0, NelBorderX, crop.size[1]))
                                                                            cropRee = crop.crop((NelBorderX - 1, 0, ReeBorderX, crop.size[1]))
                                                                                                    
                                                                            cropEsm.save("croppedEsm.png")
                                                                            cropTei.save("croppedTei.png")
                                                                            cropKol.save("croppedKol.png")
                                                                            cropNel.save("croppedNel.png")
                                                                            cropRee.save("croppedRee.png")
                                                                            
                                                                            # Create black and white mask picture for later use in the code
                                                                            colorImg = cv2.imread(IMAGENAME)
                                                                            hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

                                                                            lower = np.array([0, 5, 20])
                                                                            upper = np.array([180, 255, 255])
            
                                                                            mask = cv2.inRange(cv2.UMat(hsv), lower, upper)
                                                                            cv2.imshow("Whole picture mask", mask)
                                                                            cv2.imwrite("WholePictureMask.png", mask)
                                                                            
                                                                            # Runs compileImg from tunniplaanEditorContinue, the code continues there
                                                                            from tunniplaanCompiler import compileImg
                                                                            compileImg()
                                                                            
                                                                            
                                                                            
                                else:
                                    print("X axis color not found")

                        else: 
                            print("Something is wrong with trying to find a continuos color")
                    else: 
                        print("Something is wrong with trying to find a continuos color")
                    
                else:
                    print("Something is wrong with the color's starting edge, couldn't find the color 5px from the edge")
            
            else: 
                addY = addY + 5
                print("Color not found after 5 pixels, continuing ↓")                         

input("Ends")
