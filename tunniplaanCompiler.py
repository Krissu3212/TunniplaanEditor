def compileImg():
    # To change the amount of space between days columns, edit the gapSize variable
    
    from PIL import Image
    import cv2
    # Import the day columns from tunniplaanEditor.py, just to get the size of the columns
    from tunniplaanEditor import cropEsm, cropTei, cropKol, cropNel, cropRee
    # Import the functions from dayColumnsEditor.py
    from dayColumnsEditor import editEsmColumn
    from dayColumnsEditor import editTeiColumn
    from dayColumnsEditor import editKolColumn
    from dayColumnsEditor import editNelColumn
    from dayColumnsEditor import editReeColumn
    from dayColumnsEditor import cropTheDayNames
    
    # Execute the functions which cleanly cut out the lesson columns and leave no free space around it
    cropTheDayNames()
    editEsmColumn()
    editTeiColumn()
    editKolColumn()
    editNelColumn()
    editReeColumn()
    
    # Get column sizes
    cropEsmX = cropEsm.size[0]
    cropTeiX = cropTei.size[0]
    cropKolX = cropKol.size[0]
    cropNelX = cropNel.size[0]
    cropReeX = cropRee.size[0]
    gapSize = 30
    LessonTimesGap = 100

    
    from lessonTimesLocationFinder import edit
    edit()
    from lessonTimesLocationFinder import lessonsLocations

    # Open edited columns, their titles and lesson times
    esmEdited = Image.open("cropEsmEdited.png")
    esmTitle = Image.open("esm.png")
    teiEdited = Image.open("cropTeiEdited.png")
    teiTitle = Image.open("tei.png")
    kolEdited = Image.open("cropKolEdited.png")
    kolTitle = Image.open("kol.png")
    nelEdited = Image.open("cropNelEdited.png")
    nelTitle = Image.open("nel.png")
    reeEdited = Image.open("cropReeEdited.png")
    reeTitle = Image.open("ree.png")

    lesson1 = Image.open("lesson1.png")
    lesson2 = Image.open("lesson2.png")
    lesson3 = Image.open("lesson3.png")
    lesson4 = Image.open("lesson4.png")
    lesson5 = Image.open("lesson5.png")
    lesson6 = Image.open("lesson6.png")
    lesson7 = Image.open("lesson7.png")
    lesson8 = Image.open("lesson8.png")
    lesson9 = Image.open("lesson9.png")
    lesson10 = Image.open("lesson10.png")

    # Calculate the gap between esmTitle and esm column edge (where to exactly position the title of the column)
    esmTitleGap = int((cropEsmX - 100) / 2) # 100 is the width of the esm.png (title picture)
    teiTitleGap = int((cropTeiX - 100) / 2)
    kolTitleGap = int((cropKolX - 100) / 2)
    nelTitleGap = int((cropNelX - 100) / 2)
    reeTitleGap = int((cropReeX - 100) / 2)

    # Create a blank white image to paste the days columns on (+ 30 for the spacing at the end of the picture)
    allDaysSizeXWithGaps = 30 + LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + cropKolX + gapSize + cropNelX + gapSize + cropReeX
    daysSizeY = cropEsm.size[1]
    blank = Image.new("RGBA", (allDaysSizeXWithGaps, daysSizeY), "black")
    
    # Paste lesson times with a smart loop
    lessons = [lesson1, lesson2, lesson3, lesson4, lesson5, lesson6, lesson7, lesson8, lesson9, lesson10]
    i = 0
    for i in range(len(lessonsLocations)):
        blank.paste(lessons[i], (0, lessonsLocations[i] + teiTitle.size[1]))
        i = i + 1

    # Paste the day columns and column titles.
    blank.paste(esmTitle, (LessonTimesGap + esmTitleGap, 0))
    blank.paste(esmEdited, (LessonTimesGap, 50))
    blank.paste(teiTitle, (LessonTimesGap + cropEsmX + gapSize + teiTitleGap, 0))
    blank.paste(teiEdited, (LessonTimesGap + cropEsmX + gapSize, 50))
    blank.paste(kolTitle, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + kolTitleGap, 0))
    blank.paste(kolEdited, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize, 50))
    blank.paste(nelTitle, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + cropKolX + gapSize + nelTitleGap, 0))
    blank.paste(nelEdited, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + cropKolX + gapSize, 50))
    blank.paste(reeTitle, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + cropKolX + gapSize + cropNelX + gapSize + reeTitleGap, 0))
    blank.paste(reeEdited, (LessonTimesGap + cropEsmX + gapSize + cropTeiX + gapSize + cropKolX + gapSize + cropNelX + gapSize, 50))
    #blank.show()
    blank.save("tunniplaanValmis.png")
    exit()
    
    
    



    
    
    