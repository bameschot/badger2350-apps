from curses import *

from ereader import *

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.keypad(True)
    applicationWidth = 120

    mainWindowHeight = 10 
    
    mainWindow = newwin(mainWindowHeight, applicationWidth, 0, 0)
    mainWindow.keypad(True)

    init_pair(0, COLOR_WHITE, COLOR_BLACK)
    init_pair(1, COLOR_RED, COLOR_BLACK)
    init_pair(2, COLOR_GREEN, COLOR_BLACK)


    statusWindow = newwin(1, applicationWidth, mainWindowHeight, 0)
    

    ereader = EReader(
        "./apps/reader/books",
        "./apps/reader/user-data",
        mainWindowHeight,
        applicationWidth
    )

    ereader.loadBookTitles()

    mainWindow.clear()
    titleIdx = 0
    selectedIdx = 0
    for title in ereader.loadedTitles:
        
        mainWindow.addstr(titleIdx,0 , f'idx: {titleIdx:02d}; title: {title["title"]}',color_pair(1))
        titleIdx+=1

    mainWindow.refresh()

    mainWindow.getkey()

    ereader.loadBook(0)
    ereader.resizeScreen(applicationWidth,mainWindowHeight)
    

    # This raises ZeroDivisionError when i == 10.
    isReadingBook = True
    while isReadingBook:
        mainWindow.clear()
        statusWindow.clear()
        
        lineIdx = 0

        for line in ereader.currentPageLines():
            try:
                mainWindow.addstr(lineIdx, 0, line)
            except:
                pass
            lineIdx+=1

        mainWindow.refresh()
        
        title = ereader.currentBookmark["title"]
        pageIdx = ereader.currentBookmark["page-idx"]
        chunkIdx = ereader.currentBookmark["chunk-idx"]
        

        statusWindow.addstr(0, 0, f'[title: {title}; page: {pageIdx:04d}; chunk: {chunkIdx:04d}]',color_pair(1))
        statusWindow.refresh()

        inp = mainWindow.getkey()
        if inp == "KEY_RIGHT":
            ereader.nextPage()
        elif inp == "KEY_LEFT":
            ereader.previousPage()
        elif inp == 'E':
            isReadingBook = False


wrapper(main)