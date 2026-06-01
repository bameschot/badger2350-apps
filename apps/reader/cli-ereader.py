import math

from curses import *
from ereader import *


COLOR_PAIR_WHITE_BLACK = 1
COLOR_PAIR_RED_BLACK = 2
COLOR_PAIR_GREEN_BLACK = 3

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.keypad(True)
    
    # setup the windows and colours
    applicationWidth = 120
    mainWindowHeight = 10 
    
    mainWindow = newwin(mainWindowHeight, applicationWidth, 0, 0)
    statusWindow = newwin(1, applicationWidth, mainWindowHeight, 0)

    mainWindow.keypad(True)

    init_pair(COLOR_PAIR_WHITE_BLACK, COLOR_WHITE, COLOR_BLACK)
    init_pair(COLOR_PAIR_RED_BLACK, COLOR_RED, COLOR_BLACK)
    init_pair(COLOR_PAIR_GREEN_BLACK, COLOR_GREEN, COLOR_BLACK)

    # load the ereader with the window size
    ereader = EReader(
        "./apps/reader/books",
        "./apps/reader/user-data",
        mainWindowHeight,
        applicationWidth
    )
    ereader.loadBookTitles()

    while True:
        selectedBookIdx = bookSelectWindow(mainWindow,statusWindow,ereader)
        ereader.loadBook(selectedBookIdx)
        ereader.resizeScreen(applicationWidth,mainWindowHeight)

        readerWindow(mainWindow,statusWindow,ereader)

def bookSelectWindow(mainWindow,statusWindow,ereader:EReader):
    mainWindow.clear()
    # update status window
    statusWindow.clear()
    statusWindow.addstr(0, 0 ,f' E = exit, S = Select',COLOR_PAIR_RED_BLACK)
    statusWindow.refresh()

    selectedIdx = 0
    
    while True:
        titleIdx = 0
        mainWindow.clear()

        # print all the titles and colour the one selected index
        for title in ereader.loadedTitles:

            isSelected = titleIdx == selectedIdx
            colorPair = color_pair(COLOR_PAIR_GREEN_BLACK) if isSelected else color_pair(COLOR_PAIR_WHITE_BLACK)
            prefix = "->" if isSelected else "* "

            mainWindow.addstr(titleIdx, 0 ,f'{prefix} idx: {titleIdx:02d}; title: {title["title"]}',colorPair)
            titleIdx+=1

        mainWindow.refresh()

        # wait for input and determine to do what next
        inp = mainWindow.getkey()

        if inp == "KEY_UP":
            selectedIdx = max(selectedIdx-1,0)
        elif inp == "KEY_DOWN":
            selectedIdx = min(selectedIdx+1,len(ereader.loadedTitles)-1)
        elif inp == 'S':
            return selectedIdx

def readerWindow(mainWindow,statusWindow,ereader:EReader):
    while True:

        # write the current page to the main screen
        mainWindow.clear()
        lineIdx = 0
        for line in ereader.currentPageLines():
            try:
                mainWindow.addstr(lineIdx, 0, line,COLOR_PAIR_WHITE_BLACK)
            except:
                pass
            lineIdx+=1

        mainWindow.refresh()
        
        # update the status window
        statusWindow.clear()
        title = ereader.currentBookmark["title"]
        pageIdx = ereader.currentBookmark["page-idx"]
        chunkIdx = ereader.currentBookmark["chunk-idx"]
        
        statusWindow.addstr(0, 0, f'[title: {title}; page: {pageIdx:04d}; chunk: {chunkIdx:04d}]',color_pair(COLOR_PAIR_RED_BLACK))
        statusWindow.refresh()

        # wait for input and determine to do what next
        inp = mainWindow.getkey()
        if inp == "KEY_RIGHT":
            ereader.nextPage()
        elif inp == "KEY_LEFT":
            ereader.previousPage()
        elif inp == 'C':
            selectedChapterIdx = chapterWindow(mainWindow,statusWindow,ereader)
            if selectedChapterIdx != None:
                ereader.jumpToChapter(selectedChapterIdx)
        elif inp == 'E':
            return

def chapterWindow(mainWindow,statusWindow,ereader:EReader):
    selectedIdx = 0

    # update status window
    statusWindow.clear()
    statusWindow.addstr(0, 0 ,f' E = exit, S = Select',COLOR_PAIR_RED_BLACK)
    statusWindow.refresh()

    while True:

        # write the current page to the main screen
        mainWindow.clear()
        chapterIdx = 0
        for chapter in ereader.currentBookMetaData["chapters"]:
            try:
                isSelected = chapterIdx == selectedIdx
                colorPair = color_pair(COLOR_PAIR_GREEN_BLACK) if isSelected else color_pair(COLOR_PAIR_WHITE_BLACK)
                prefix = "->" if isSelected else "* "

                mainWindow.addstr(chapterIdx, 0, f'{prefix} {chapter["title"]}',colorPair)
            except:
                pass
            chapterIdx+=1

        mainWindow.refresh()


        # wait for input and determine to do what next
        inp = mainWindow.getkey()
        if inp == "KEY_UP":
            selectedIdx = max(selectedIdx-1,0)
        elif inp == "KEY_DOWN":
            selectedIdx = min(selectedIdx+1,len(ereader.currentBookMetaData["chapters"])-1)
        elif inp == 'S':
            return selectedIdx
        elif inp == 'E':
            return None

wrapper(main)