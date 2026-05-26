

#file format
# metadata (json)
#  -> title
#  -> author
#  -> year 
#  -> publisher
# chunk-info
#  -> total
#  -> chunk-size (bytes)



# gzip single file
# chunks
#


#load file


#

import deflate, json

# Write a dictionary as JSON in gzip format, with a
# small (64 byte) window size.
config = { "item", "1"}
with open("config.gz", "wb") as f:
    with deflate.DeflateIO(f, deflate.GZIP, 6) as f:
        json.dump(config, f)

# Read back that dictionary.
with open("config.gz", "rb") as f:
    with deflate.DeflateIO(f, deflate.GZIP, 6) as f:
        config = json.load(f)
        print(config)