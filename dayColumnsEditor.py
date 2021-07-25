# Edit every day's column separately in their own function.
# First function (esm) is with comments, the code for other functions are all the same

from PIL import Image
import cv2
import numpy as np
import pytesseract

from tunniplaanEditor import firstColorLocation

# Crop the day names from the top of the columnns. This could have been done earlier when the columns were all as one picture, and more shorter, but i'm doing it here for simplicity.
def cropTheDayNames():
    esm = Image.open("croppedEsm.png")
    # - 1 to select also the 1 pixel wide border
    esmCropped = esm.crop((0, firstColorLocation[1] - 1, esm.size[0], esm.size[1]))
    esmCropped.save("croppedEsm.png")

    tei = Image.open("croppedTei.png")
    teiCropped = tei.crop((0, firstColorLocation[1] - 1, tei.size[0], tei.size[1]))
    teiCropped.save("croppedTei.png")

    kol = Image.open("croppedKol.png")
    kolCropped = kol.crop((0, firstColorLocation[1] - 1, kol.size[0], kol.size[1]))
    kolCropped.save("croppedKol.png")

    nel = Image.open("croppedNel.png")
    nelCropped = nel.crop((0, firstColorLocation[1] - 1, nel.size[0], nel.size[1]))
    nelCropped.save("croppedNel.png")

    ree = Image.open("croppedRee.png")
    reeCropped = ree.crop((0, firstColorLocation[1] - 1, ree.size[0], ree.size[1]))
    reeCropped.save("croppedRee.png")


def editEsmColumn():

    # Changes all white colors to black
    esm = Image.open("croppedEsm.png")
    esmSize = esm.size
    #color_to_find2 = (0, 0, 0, 255)
    color_to_find1 = (255, 255, 255, 255)
    #color_to_replace2 = (255, 255, 255, 255)
    color_to_replace1 = (0, 0, 0, 255)
    
    new_image_data = []
    
    for color in list(esm.getdata()):
        if (color == color_to_find1):
            new_image_data += [color_to_replace1]
        #elif (color == color_to_find2):
            #new_image_data += [color_to_replace2]
        else:
            new_image_data += [color]
    esm.putdata(new_image_data)

    # Get non-white and non-black colors (Create the black and white image)
    colorImg = cv2.imread("croppedEsm.png")
    hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 5, 50])
    upper = np.array([179, 255, 255])
    
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imwrite("esmMask.png", mask) # Save the mask with cv2 because PIL can't use cv2 edited image directly
    
    # Start from the bottom of the whole image to find the last lesson of the day's column by searching for white color (as done in the previous code too)
    esmMaskOpen = Image.open("esmMask.png") # Open the mask image with PIL
    esmMask = esmMaskOpen.load()
    add = 0
    while add < 400:
        add = add + 1
        # Subtract - 50 to not start the pixel checking at the very edge. Couldn't divide by 2, because it would give back a float and the function doesn't accept floats.
        # Check if the color found is continuous
        print(esmSize[0] - 50, esmSize[1] - add)
        if (esmMask[esmSize[0] - 50, esmSize[1] - add] == 255):
            if (esmMask[esmSize[0] - 50, esmSize[1] - add - 3] == 255):
                if (esmMask[esmSize[0] - 50, esmSize[1] - add - 5] == 255):
                    if (esmMask[esmSize[0] - 50, esmSize[1] - add - 7] == 255):
                        print("First esm color from below found at " + str(esmSize[0] - 50), str(esmSize[1] - add))
                        esmBottomBorderY = esmSize[1] - add

                        crop = esm
                        # Crop the day's column from the bottom that the code just found (esmBottomBorderY)
                        # + 2 to select also the 1 pixel wide border
                        croppedEsm = crop.crop((0, 0, esmSize[0], esmBottomBorderY + 2))
                        print("Cropping done")
                        
                        croppedEsm.save("cropEsmEdited.png")
                        break # To stop the image cropping cycle
                    

def editTeiColumn():

    tei = Image.open("croppedTei.png")
    teiSize = tei.size
    color_to_find1 = (255, 255, 255, 255) 
    color_to_replace1 = (0, 0, 0, 255)
    
    new_image_data = []
    
    for color in list(tei.getdata()):
        if (color == color_to_find1):
            new_image_data += [color_to_replace1]
        else:
            new_image_data += [color]
    tei.putdata(new_image_data)

    colorImg = cv2.imread("croppedTei.png")
    hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 5, 50])
    upper = np.array([179, 255, 255])
    
    cv2mask = cv2.inRange(hsv, lower, upper)
    cv2.imwrite("teiMask.png", cv2mask)
    
    maskOpen = Image.open("teiMask.png") 
    mask = maskOpen.load()
    add = 0
    while add < 400:
        add = add + 1
        print(teiSize[0] - 50, teiSize[1] - add)
        if (mask[teiSize[0] - 50, teiSize[1] - add] == 255):
            if (mask[teiSize[0] - 50, teiSize[1] - add - 3] == 255):
                if (mask[teiSize[0] - 50, teiSize[1] - add - 5] == 255):
                    if (mask[teiSize[0] - 50, teiSize[1] - add - 7] == 255):
                        print("First tei color from below found at " + str(teiSize[0] - 50), str(teiSize[1] - add))
                        teiBottomBorderY = teiSize[1] - add

                        crop = tei
                        croppedTei = crop.crop((0, 0, teiSize[0], teiBottomBorderY + 2))
                        
                        croppedTei.save("cropTeiEdited.png")
                        break
                       

def editKolColumn():
    
    kol = Image.open("croppedKol.png")
    kolSize = kol.size
    color_to_find1 = (255, 255, 255, 255)
    color_to_replace1 = (0, 0, 0, 255)
    
    new_image_data = []
    
    for color in list(kol.getdata()):
        if (color == color_to_find1):
            new_image_data += [color_to_replace1]
        else:
            new_image_data += [color]
    kol.putdata(new_image_data)

    colorImg = cv2.imread("croppedKol.png")
    hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 5, 50])
    upper = np.array([179, 255, 255])
    
    cv2mask = cv2.inRange(hsv, lower, upper)
    cv2.imwrite("kolMask.png", cv2mask)
    
    maskOpen = Image.open("kolMask.png")
    mask = maskOpen.load()
    add = 0
    while add < 400:
        add = add + 1
        print(kolSize[0] - 50, kolSize[1] - add)
        if (mask[kolSize[0] - 50, kolSize[1] - add] == 255):
            if (mask[kolSize[0] - 50, kolSize[1] - add - 3] == 255):
                if (mask[kolSize[0] - 50, kolSize[1] - add - 5] == 255):
                    if (mask[kolSize[0] - 50, kolSize[1] - add - 7] == 255):
                        print("First kol color from below found at " + str(kolSize[0] - 50), str(kolSize[1] - add))
                        kolBottomBorderY = kolSize[1] - add

                        crop = kol
                        croppedKol = crop.crop((0, 0, kolSize[0], kolBottomBorderY + 2))
                        
                        croppedKol.save("cropKolEdited.png")
                        break

def editNelColumn():
    
    nel = Image.open("croppedNel.png")
    nelSize = nel.size
    color_to_find1 = (255, 255, 255, 255)
    color_to_replace1 = (0, 0, 0, 255)
    
    new_image_data = []
    
    for color in list(nel.getdata()):
        if (color == color_to_find1):
            new_image_data += [color_to_replace1]
        else:
            new_image_data += [color]
    nel.putdata(new_image_data)

    colorImg = cv2.imread("croppedNel.png")
    hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 5, 50])
    upper = np.array([179, 255, 255])
    
    cv2mask = cv2.inRange(hsv, lower, upper)
    cv2.imwrite("nelMask.png", cv2mask)
    
    maskOpen = Image.open("nelMask.png")
    mask = maskOpen.load()
    add = 0
    while add < 400:
        add = add + 1
        print(nelSize[0] - 50, nelSize[1] - add)
        if (mask[nelSize[0] - 50, nelSize[1] - add] == 255):
            if (mask[nelSize[0] - 50, nelSize[1] - add - 3] == 255):
                if (mask[nelSize[0] - 50, nelSize[1] - add - 5] == 255):
                    if (mask[nelSize[0] - 50, nelSize[1] - add - 7] == 255):
                        print("First nel color from below found at " + str(nelSize[0] - 50), str(nelSize[1] - add))
                        nelBottomBorderY = nelSize[1] - add

                        crop = nel
                        croppedNel = crop.crop((0, 0, nelSize[0], nelBottomBorderY + 2))
                        
                        croppedNel.save("cropNelEdited.png")
                        break

def editReeColumn():
    
    ree = Image.open("croppedRee.png")
    reeSize = ree.size
    color_to_find1 = (255, 255, 255, 255)
    color_to_replace1 = (0, 0, 0, 255)
    
    new_image_data = []
    
    for color in list(ree.getdata()):
        if (color == color_to_find1):
            new_image_data += [color_to_replace1]
        else:
            new_image_data += [color]
    ree.putdata(new_image_data)

    colorImg = cv2.imread("croppedRee.png")
    hsv = cv2.cvtColor(colorImg, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 5, 50])
    upper = np.array([179, 255, 255])
    
    cv2mask = cv2.inRange(hsv, lower, upper)
    cv2.imwrite("reeMask.png", cv2mask)
    
    maskOpen = Image.open("reeMask.png")
    mask = maskOpen.load()
    add = 0
    while add < 400:
        add = add + 1
        print(reeSize[0] - 50, reeSize[1] - add)
        if (mask[reeSize[0] - 50, reeSize[1] - add] == 255):
            if (mask[reeSize[0] - 50, reeSize[1] - add - 3] == 255):
                if (mask[reeSize[0] - 50, reeSize[1] - add - 5] == 255):
                    if (mask[reeSize[0] - 50, reeSize[1] - add - 7] == 255):
                        print("First ree color from below found at " + str(reeSize[0] - 50), str(reeSize[1] - add))
                        reeBottomBorderY = reeSize[1] - add

                        crop = ree
                        croppedRee = crop.crop((0, 0, reeSize[0], reeBottomBorderY + 2))
                        
                        croppedRee.save("cropReeEdited.png")
                        break

# Just copy pasta right ?!