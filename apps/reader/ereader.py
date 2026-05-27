import os

from picobook import *


# USER FILE
# -> last-book
#   -> title
#   -> last-chunk
#   -> last-line

# BOOKMARK FILE
# -> bookmark
#   -> title
#   -> last-chunk
#   -> last-line

class EReader:
    def __init__(self, booksDirectory, userDataDirectory, linesPerScreen, charactersPerLine):
        self.booksDirectory = booksDirectory
        self.userDataDirectory = userDataDirectory
        self.linesPerScreen = linesPerScreen
        self.charactersPerLine = charactersPerLine

        self.loadedTitles = []

        self.currentBookMetaData = None
        self.currentBookChunkIdx = None
        self.currentPageLine = None
        self.currentPageViewLines = []


    def loadTitles(self):
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
    
    def loadBook(self,idx):
        """
        load a book based on the index of the loaded book and set the book the last read position from the userfile or create a new 
        """ 
        with open(self.loadedTitles[idx]["path"],"rb") as picobook:
            self.currentBookMetaData = readPicoBookMetaData(picobook)
            self.currentBookChunkIdx = 0
            self.setCurrentPageViewLinesFromText(readPicoBookChunks(picobook, self.currentBookMetaData,self.currentBookChunk,1))
            self.currentPageLine = 0

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
                






        


ereader = EReader(
    "./apps/reader/books",
    "./apps/reader/user-data",
    10,
    80
)

ereader.loadTitles()
ereader.loadBook(0)    

print("----")
for line in ereader.currentPageViewLines:
    print(line)
    