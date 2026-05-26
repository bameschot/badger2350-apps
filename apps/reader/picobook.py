import json 
import gzip

# FILE STRUCTURE
#  1. MAGIC_BYTES (4 bytes) = sanity check to detect picobook format (0xA4,0xB4,0xC4,0xD4)
#  2. VERSION (2 bytes) = version number of the picobook scheme (0x00,0x01)
#  3. META_DATA_LENGTH (4 bytes) = length of the meta data structure in bytes  (integer)
#  4. START_CHUNK_BYTE_IDX (4 bytes) = index if the position of the first byte of the first chunk (integer)
#  5. META_DATA (n bytes) = gzipped json structure containing the books meta data (see JSON META DATA)
#  5. CHUNKS (n bytes) = The gzipped text contents of the book (see CHUNK STRUCTURE)
 
# CHUNK STRUCTURE
#  1. CHUNK_INDEX (4 bytes) = the index of the chunk (integer)
#  2. CHUNK_COMPRESSED_SIZE_BYTES (4 bytes) = size in bytes of the compressed data (integer)
#  3. CHUNK_DATA (n bytes) = the gzipped text data of the chunk

#JSON META DATA
# metadata (json)
#	-> title
#  	-> author
# 	-> year 
#  	-> publisher
#	-> [chapters]?
#       -> [chapter]*
#           -> idx
#			-> title
#			-> chunk-start-idx    
#  -> [chunks]
#  		-> chunk-total
#  		-> content-size-bytes
#       -> chunk-start-positions list:int

PICOBOOK_EXTENTION = ".pb"
PICOBOOK_STR_ENCODING = "utf-8"

PICOBOOK_PICOBOOK_MAGIC_BYTES = bytes([0xa4,0xb4,0xc4,0xd4])
PICOBOOK_PICOBOOK_VERSION_BYTES = bytes([0x00,0x01])

def compress(uncompressedBytes):
    return gzip.compress(uncompressedBytes,compresslevel=6)

def decompress(compressedBytes):
    return gzip.decompress(compressedBytes)

def createMetadata(
    title,    
    author = None,
    publisher = None,
    year = None,
    chaptersDict = None,
    chunkInfoDict = None
):
    metaData = {
        "title": title        
    }

    if author != None:
        metaData["author"] = author
    if publisher != None:
        metaData["publisher"] = publisher
    if year != None:
        metaData["author"] = year
    if chaptersDict != None:
        metaData["chapters"] = chaptersDict
    if chunkInfoDict != None:
        metaData["chunk-info"] = chunkInfoDict

    return json.dumps(metaData)


def createChunk(inputBytes,chunkIdx):
    chunkIdxBytes = chunkIdx.to_bytes(4)
    compressedBytes = compress(inputBytes)
    compressedSizeBytes = len(compressedBytes).to_bytes(4)
    print(f'chunk index: {chunkIdx:06d} chunk index bytes: {len(chunkIdxBytes)}b compressed size bytes: {len(compressedSizeBytes)}b chunk size: {len(compressedBytes):05d}')
    
    # create the chunk and return the size of the chunk in bytes and the chunk itself as a dictionary
    chunk = chunkIdxBytes + compressedSizeBytes + compressedBytes
    return chunk


def convertTxtFileToPicoBook(
    inputStream,
    outputStream,
    title,
    author = None,
    publisher = None,
    year = None,
    contentSizeBytes = 1024*10):

    chunkInfoDict = {
        "chunk-total": 0,
        "content-size-bytes": contentSizeBytes,
        "chunk-start-indexes": []
    }


    # create the chunks and fill in the chunk data
    chunkIdx = 0
    lastChunkStartIndex = 0
    chunks = []

    # read the input file
    while(True):
        inputBytes = inputStream.read(contentSizeBytes)
        if len(inputBytes)<=0:
            break
        
        # create the chunk
        chunkBytes = createChunk(inputBytes,chunkIdx)
        chunks.append(chunkBytes)

        # register this chunk's starting index in the metadata
        newChunkStartIndex = lastChunkStartIndex+len(chunkBytes)
        chunkInfoDict["chunk-start-indexes"].append(lastChunkStartIndex)
        lastChunkStartIndex=newChunkStartIndex
        
        chunkIdx+=1
    
    # register the total amount of chunks in the book
    chunkInfoDict["chunk-total"]=chunkIdx

    # create and compress the meta data
    metaData = createMetadata(
                title=title,
                author=author,
                publisher=publisher,
                year=year,
                chaptersDict=None,
                chunkInfoDict=chunkInfoDict
            )
    
    writePicoBook(outputStream,metaData,chunks)
        

def writePicoBook(picoBookStream,metaData,chunks):
    metaDataBytes = compress(bytes(metaData,PICOBOOK_STR_ENCODING)) 
    print(f"metadata: {metaData}")

    # calculate the start of the chunk section (add 8 for the meta data size and chunk start index integers itself)
    startChunkByteIdx = len(PICOBOOK_PICOBOOK_MAGIC_BYTES) +len(PICOBOOK_PICOBOOK_VERSION_BYTES)+len(metaDataBytes)+8

    # create the picobook file
    picoBookStream.write(PICOBOOK_PICOBOOK_MAGIC_BYTES)
    picoBookStream.write(PICOBOOK_PICOBOOK_VERSION_BYTES)
    picoBookStream.write(len(metaDataBytes).to_bytes(4))
    picoBookStream.write(startChunkByteIdx.to_bytes(4))
    picoBookStream.write(metaDataBytes)
    for chunk in chunks:
        picoBookStream.write(chunk)


def readChunk(picoBookStream):
    # read the chunk index and the size of the compressed dat in the chunk in bytes
    chunkIdx = int.from_bytes(picoBookStream.read(4))
    compressedSizeBytes = int.from_bytes(picoBookStream.read(4))

    print(f"chunk: {chunkIdx:06d} compressed size: {compressedSizeBytes:08d}b")

    # decompress the data and turn it into a string
    chunkBytes = decompress(picoBookStream.read(compressedSizeBytes))
    return chunkBytes.decode(PICOBOOK_STR_ENCODING,"replace")

def readPicoBookHeader(picoBookStream,readMetaData=True):
    # read and validate the magic bytes
    picobookMagicBytes = picoBookStream.read(len(PICOBOOK_PICOBOOK_MAGIC_BYTES))
    if picobookMagicBytes != PICOBOOK_PICOBOOK_MAGIC_BYTES:
        raise Exception(f'file is not a picobook, wrong magic bytes {picobookMagicBytes} vs required {PICOBOOK_PICOBOOK_MAGIC_BYTES}')
        
    # read the version
    picobookVersion = int.from_bytes(picoBookStream.read(2))
    print(f"version: {picobookVersion}")

    # read the metadata size
    metaDataSizeInBytes = int.from_bytes(picoBookStream.read(4))
    print(f"meta data size (bytes): {metaDataSizeInBytes}")

    # read the chunk start position
    chunkStartIdx = int.from_bytes(picoBookStream.read(4))
    print(f"chunk start idx: {chunkStartIdx}")

    # read and decompress the metadata
    if readMetaData:
        metaData = json.loads(decompress(picoBookStream.read(metaDataSizeInBytes)))
    else:
        # just skip over the bytes
        picoBookStream.read(metaDataSizeInBytes)
        metaData = None
    print(f"meta data: {metaData}")


    return {
        "version": picobookVersion,
        "meta-data-size-bytes": metaDataSizeInBytes,
        "chunk-start-index": chunkStartIdx,
        "meta-data": metaData
    }
    

def readPicoBook(picoBookFilePath):
    with open(picoBookFilePath,"rb") as picoBook:

        # read the picobook header
        header = readPicoBookHeader(picoBook)
        metaData = header["meta-data"]

        # read the chunks and append the text to the total book
        text = ""
        for _ in range(0 , metaData["chunk-info"]["chunk-total"]):
            text+=readChunk(picoBook)
        
        return {"meta-data":metaData,"text": text}
    
def readPicoBookMetaData(picoBookStream):
        # read the picobook header
        return readPicoBookHeader(picoBookStream)["meta-data"]

    
def readPicoBookChunks(picoBookStream,metaData=None,chunkIdx=0,chunksToRead=None):
    # reset, function assumes it starts from the beginning of the file
    picoBook.seek(0)

    # read the picobook header, ommit parsing the meta data if indicated
    header = readPicoBookHeader(picoBookStream,False if metaData!=None else True)
    metaData = header["meta-data"] if metaData == None else metaData 

    chunkBytesStartIndex = header["chunk-start-index"]
    totalChunks = metaData["chunk-info"]["chunk-total"]
    
    # calculate the requested chunk range and check if it is in range
    chunkStartIndex = chunkIdx
    chunkEndIndex = chunkIdx + chunksToRead if chunksToRead != None else totalChunks-chunkIdx

    if chunkStartIndex < 0 or (chunkEndIndex) > totalChunks:
        raise Exception(f'requested chunks: {chunkStartIndex} to {chunkEndIndex} are not in range (0 < n > {totalChunks})')

    # find the correct start of the chunk by retrieving the start index for the indicated chunk idx
    chunkStartPosition = chunkBytesStartIndex + metaData["chunk-info"]["chunk-start-indexes"][chunkStartIndex]
    picoBookStream.seek(chunkStartPosition)

    # read and return the chunk
    chunkText = ""
    for _ in range(chunkStartIndex,chunkEndIndex):
        chunkText += readChunk(picoBookStream)
    return chunkText
            

# write
with open('./king-in-yellow.txt', "rb") as inputFile:
    with open('./king-in-yellow.pb', "wb") as outputFile:
        convertTxtFileToPicoBook(inputFile,outputFile,'king in yellow')


# read
with open('./king-in-yellow.pb',"rb") as picoBook:
    picobookFull = readPicoBook("./king-in-yellow.pb")
    print(picobookFull["text"])
    print(picobookFull["meta-data"])
print("--------")


with open('./king-in-yellow.pb',"rb") as picoBook:
    chunkTxt = readPicoBookChunks(picoBook, picobookFull["meta-data"],41,1)
    print(chunkTxt)
print("--------")

with open('./king-in-yellow.pb',"rb") as picoBook:
    # read meta data 
    metaData = readPicoBookMetaData(picoBook)
    # read the entire book's chunks
    text = readPicoBookChunks(picoBook,metaData)
    print(text)
    print(metaData)

with open('./king-in-yellow.pb',"rb") as picoBook:
    print(readPicoBookChunks(picoBook))






