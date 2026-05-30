import os

from picobook import *


BOOKMARKS_FILE_NAME = "bookmarks.json"

# BOOKMARKS FILE
# -> bookmarks
#   -> [bookmark]*
#       -> title
#       -> chunk-idx
#       -> page-idx
#       -> characters-per-line
#       -> lines-per-page

class EReader:
    def __init__(self, booksDirectory, userDataDirectory, linesPerScreen, charactersPerLine):
        self.booksDirectory = booksDirectory
        self.userDataDirectory = userDataDirectory
        self.defaultLinesPerPage = linesPerScreen
        self.defaultCharactersPerLine = charactersPerLine

        self.loadedTitles = []
        self.bookmarks = None

        self.viewPages = None

        self.currentBookmark = None
        self.currentBookMetaData = None


    def loadBookTitles(self):
        """
        load a all titles available in the books directory and store them indexed with the path to the book

        :return: None
        """ 
        for file in os.listdir(self.booksDirectory):
            if PICOBOOK_EXTENTION in file:
                path = self.booksDirectory+"/"+file
                with open(path,"rb") as picobook:
                    metaData = readPicoBookMetaData(picobook)
                self.loadedTitles.append({
                        "title": metaData["title"],
                        "path": self.booksDirectory+"/"+file
                    })
                del metaData
            
        print(self.loadedTitles)
        self.loadBookmarks()
    
    def loadBook(self,bookIdx):
        """
        load a book based on the index of the loaded book and set the book the last read position from the bookmark

        :param bookIdx: the index of the book in the loaded titles to load 

        :return: None
        """ 
        # open the file indicated by the index
        with open(self.loadedTitles[bookIdx]["path"],"rb") as picobook:

            # load the book's bookmark based on the tile
            self.currentBookmark = self.findBookmark(self.loadedTitles[bookIdx]["title"])

            # load the book's meta data 
            self.currentBookMetaData = readPicoBookMetaData(picobook)

            # load the bookmarked chunk and paginate it according to the bookmark's settings
            self.viewPages = self.paginateLines(
                self.readLinesFromText(
                    readPicoBookChunks(picobook, self.currentBookMetaData,self.currentBookmark["chunk-idx"],1),
                    self.currentBookmark["characters-per-line"]
                ),self.currentBookmark["lines-per-page"]
            )

    def resetStream(self,stream):
        """
        clears and resets a given stream 
        
        :param stream: the stream to clear

        :return: the cleared stream

        """ 
        stream.truncate(0)
        stream.seek(0)
        return stream

    def readLinesFromText(self,text,charactersPerLine):
        """
        reads the given text into lines taking into account the character width of the ereader

        :param text: the text to parse into lines 
        :param charactersPerLine: the number of characters allowed per line

        :return: a the text as a list of lines
        """ 
        lines = []
        currentLine = io.StringIO()
        self.distributeTokensIntoLines(text.split(' '),charactersPerLine,lines ,currentLine)
        
        return lines
    

    def distributeTokensIntoLines(self,tokens,charactersPerLine,lines,currentLineStream):
        """
        Distributes a given whitespace tokenized text in lines taking into account the maximum line length, lines are added to the lines paramer

        :param tokens: a list of individual tokens (text split on ' ') that needs to be distrubuted across lines
        :param charactersPerLine: the number of characters allowed per line
        :param lines: a list of lines to add the result lines to
        :currentLineStream: a stream object that is used as a stringbuffer to add tokens to a line to

        :return: None 
        """
        for token in tokens:
            # if there is a newline in the token split the token
            if '\n' in token:
                nwlnSplit = token.split('\n')
                # just a single newline 
                if len(nwlnSplit) == 0:
                    lines.append(currentLineStream.getvalue())
                    self.resetStream(currentLineStream)
                # word split by newlines, add these individually
                else:
                    self.distributeTokensIntoLines(nwlnSplit,charactersPerLine,lines,currentLineStream)
            # split tokens that are too large into multiple tokens and add these individually
            elif len(token) > self.defaultCharactersPerLine:
                oversizedTokens = [token[x:x+self.defaultCharactersPerLine-1]+'-' for x in range(0,len(token),self.defaultCharactersPerLine-1)]
                self.distributeTokensIntoLines(oversizedTokens,charactersPerLine,lines,currentLineStream)
            # if appending the token (and the whitespace after) causes the line to overflow add the line and start a new one with the token
            elif len(token)>0 and currentLineStream.tell()+len(token)+1> self.defaultCharactersPerLine:
                lines.append(currentLineStream.getvalue())
                self.resetStream(currentLineStream)
                currentLineStream.write(token) 
                currentLineStream.write(' ') 
            # otherwise just add the token
            elif len(token)>0:
                    currentLineStream.write(token) 
                    currentLineStream.write(' ')

    def paginateLines(self,lines,linesPerPage):
        """
        paginates the given lines into a list of pages taking into account the maximum amount of lines allowed per screen

        :param lines: a list of lines containing the text
        :param linesPerPage: number of lines allowed per page

        :return: a list of `pages` that themselves contain a list of lines per page (string[][])
        """
        pages = []
        pages.append([])
        lineIdx=0
        pageIdx=0
        for line in lines:
            if lineIdx % linesPerPage == 0:
                pages.append([])
                pageIdx+=1

            pages[pageIdx].append(line)
            lineIdx+=1
        
        return pages
    

    def loadBookmarks(self):
        """
        load (and create if not exists) the bookmarks file and add a new bookmark for any title that does not exist yet

        :return: None
        """
        bookmarksFilePath = self.userDataDirectory+"/"+BOOKMARKS_FILE_NAME

        # check if the file exists, and if not create a new one
        if not os.path.exists(bookmarksFilePath):
            with open(bookmarksFilePath,"w") as bookmarksFile:
                json.dump({"bookmarks":[]},bookmarksFile)

        # read the bookmarks file
        with open(bookmarksFilePath,"r") as bookmarksFile:
            bookmarks = json.load(bookmarksFile)
        
        self.bookmarks = bookmarks["bookmarks"]




    def findBookmark(self,title):
        """
        finds a loaded bookmark by title

        :param title: the title of the book to find the bookmark for 

        :return: the Bookmark found
        """
        for bookmark in self.bookmarks:
            if bookmark["title"] == title:
                return bookmark
        
        # not found, create and append a new bookmark
        newBookmark = self.createBookmark(title,0,0,self.defaultCharactersPerLine,self.defaultLinesPerPage)
        self.bookmarks.append(newBookmark)

        # store the new bookmark in the file
        self.saveBookmarks()

        return newBookmark
    
    def saveBookmarks(self):
        """
        Stores the current bookmarks into the bookmarks file
        """
        bookmarksFilePath = self.userDataDirectory+"/"+BOOKMARKS_FILE_NAME
        with open(bookmarksFilePath,"w") as bookmarksFile:
            json.dump(self.bookmarks,bookmarksFile)
        
    def createBookmark(self, title, chunkIdx, pageIdx, charactersPerLine, linesPerPage):
        """
        Create a bookmark dictionary

        :return: the Bookmark dictionary
        """
        return {
            "title": title,
            "chunk-idx": chunkIdx,
            "page-idx": pageIdx,
            "characters-per-line": charactersPerLine,
            "lines-per-page": linesPerPage,
        }

                    

ereader = EReader(
    "./apps/reader/books",
    "./apps/reader/user-data",
    10,
    70
)

ereader.loadBookTitles()
ereader.loadBook(0)    

for page in ereader.viewPages:
    for line in page:
        print(line)
    print("------------")
    