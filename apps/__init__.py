
# select a font to use
screen.font = rom_font.nope


def init():
    badge.update()
    bounds = rect(10, 10, 140, 110)
    message = "WWell hello there, world! This is a nice long message that's designed to split over several lines, so I'm just going to ramble on for a little while."
    text.draw(screen, message, bounds)
    
    badge.update()



def update():
    pass
    #bounds = rect(10, 10, 140, 110)
    #message = "Well hello there, world! This is a nice long message that's designed to split over several lines, so I'm just going to ramble on for a little while."
    #text.draw(screen, message, bounds)
    
    #badge.update()

def on_exit():
    pass


init()





