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
    

    # This raises ZeroDivisionError when i == 10.
    isReadingBook = True
    while isReadingBook:
        mainWindow.clear()
        statusWindow.clear()
        
        lineIdx = 0
        for line in ereader.currentPageLines():
            mainWindow.addstr(lineIdx, 0, line)
            lineIdx+=1

        mainWindow.refresh()
        inp = mainWindow.getch()
        statusWindow.addstr(0, 0, str(ereader.currentBookmark))
        statusWindow.refresh()

        if inp == KEY_RIGHT:
            ereader.nextPage()
        elif inp == KEY_LEFT:
            ereader.previousPage()
        elif inp == 'E':
            isReadingBook = False


wrapper(main)