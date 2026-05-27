import os

from picobook import *


BOOKMARKS_FILE_NAME = "bookmarks.json"

# BOOKMARKS FILE
# -> bookmarks
#   -> [bookmark]*
#       -> title
#       -> chunk-idx
#       -> line

class EReader:
    def __init__(self, booksDirectory, userDataDirectory, linesPerScreen, charactersPerLine):
        self.booksDirectory = booksDirectory
        self.userDataDirectory = userDataDirectory
        self.linesPerScreen = linesPerScreen
        self.charactersPerLine = charactersPerLine

        self.loadedTitles = []
        self.bookmarks = None

        self.currentBookmark = None
        self.currentBookMetaData = None
        self.currentPageViewLines = []


    def loadBookTitles(self):
        """
        load a all titles available in the books directory and store them indexed with the path to the book
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
    
    def loadBook(self,idx):
        """
        load a book based on the index of the loaded book and set the book the last read position from the bookmark
        """ 
        with open(self.loadedTitles[idx]["path"],"rb") as picobook:
            self.currentBookMetaData = readPicoBookMetaData(picobook)
            self.currentBookmark = self.findBookmark(self.loadedTitles[idx]["title"])
            self.setCurrentPageViewLinesFromText(
                readPicoBookChunks(picobook, self.currentBookMetaData,self.currentBookmark["chunk-idx"],1)
            )

    def resetStream(self,stream):
        """
        clears and resets a given stream 
        """ 
        stream.truncate(0)
        stream.seek(0)

    def setCurrentPageViewLinesFromText(self,text):
        """
        sets the page view lines based on the given raw text
        """ 
        del self.currentPageViewLines
        self.currentPageViewLines = []
        currentLine = io.StringIO()
        self.distributeTokensIntoLines(text.split(' '),self.currentPageViewLines ,currentLine)        

    
    def distributeTokensIntoLines(self,tokens,lines,currentLineStream):
        """
        Distributes a given whitespace tokenized text in lines taking into account the maximum line length
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
                    self.distributeTokensIntoLines(nwlnSplit,lines,currentLineStream)
            # split tokens that are too large into multiple tokens and add these individually
            elif len(token) > self.charactersPerLine:
                oversizedTokens = [token[x:x+self.charactersPerLine] for x in range(0,len(token),self.charactersPerLine)]
                self.distributeTokensIntoLines(oversizedTokens,lines,currentLineStream)
            # if appending the token (and the whitespace after) causes the line to overflow add the line and start a new one with the token
            elif len(token)>0 and currentLineStream.tell()+len(token)+1> self.charactersPerLine:
                lines.append(currentLineStream.getvalue())
                self.resetStream(currentLineStream)
                currentLineStream.write(token) 
                currentLineStream.write(' ') 
            # otherwise just add the token
            elif len(token)>0:
                    currentLineStream.write(token) 
                    currentLineStream.write(' ')

    def loadBookmarks(self):
        """
        load (and create if not exists) the bookmarks file and add a new bookmark for any title that does not exist yet
        """
        bookmarksFilePath = self.userDataDirectory+"/"+BOOKMARKS_FILE_NAME

        # check if the file exists, and if not create a new one
        if not os.path.exists(bookmarksFilePath):
            with open(bookmarksFilePath,"w") as bookmarksFile:
                json.dump({"bookmarks":[]},bookmarksFile)

        # read the bookmarks file
        with open(bookmarksFilePath,"r") as bookmarksFile:
            bookmarks = json.load(bookmarksFile)
        
        # for each title check if the bookmarks file exists and create an empty entry if it does not
        modifiedBookmarks = False
        for title in self.loadedTitles:
            bookmarkExists = False
            for bookmark in bookmarks["bookmarks"]:
                if title["title"] in bookmark["title"]:
                    bookmarkExists = True
                    break 
            if not bookmarkExists:
                bookmarks["bookmarks"].append(self.createBookmark(title["title"],0,0))
                modifiedBookmarks = True

        # if the bookmarks where modified during the loading write them out again
        if modifiedBookmarks:
            with open(bookmarksFilePath,"w") as bookmarksFile:
                json.dump(bookmarks,bookmarksFile)

        self.bookmarks = bookmarks["bookmarks"]

    def findBookmark(self,title):
        """
        finds a loaded bookmark by title
        """
        for bookmark in self.bookmarks:
            if bookmark["title"] == title:
                return bookmark
        raise Exception(f"bookmark for title {title} not found")

 
    def createBookmark(self, title, chunkIdx, line):
        """
        Create a bookmark dictionary
        """
        return {
            "title": title,
            "chunk-idx": chunkIdx,
            "line": line
        }
    
    def nextPage(self):
        currentLine = self.currentBookmark["line"]
        

    def previousPage(self):
        pass

                    

ereader = EReader(
    "./apps/reader/books",
    "./apps/reader/user-data",
    10,
    80
)

ereader.loadBookTitles()
ereader.loadBook(0)    

print("----")
for line in ereader.currentPageViewLines:
    print(line)
    