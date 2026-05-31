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

    statusWindow = newwin(1, applicationWidth, mainWindowHeight, 0)

    ereader = EReader(
        "./apps/reader/books",
        "./apps/reader/user-data",
        mainWindowHeight,
        applicationWidth
    )

    ereader.loadBookTitles()
    ereader.loadBook(0)
    ereader.resizeScreen(applicationWidth,mainWindowHeight)
    init_pair(1, COLOR_RED, COLOR_BLACK)
    

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

        inp = mainWindow.getch()
        if inp == KEY_RIGHT:
            ereader.nextPage()
        elif inp == KEY_LEFT:
            ereader.previousPage()
        elif inp == 'E':
            isReadingBook = False


wrapper(main)