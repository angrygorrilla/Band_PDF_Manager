

#get the list of all letters between 2 letters
def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters.""" 
    for ord_ in range(ord(start.lower()), ord(stop.lower()), step):
        yield chr(ord_)
        
#flatten a list of lists        
def flatten(xss):
    return [x for xs in xss for x in xs] 
        
#return the list of all possible key signatures, all in lower case
#not all keys are logical, but they're all included here
key_signatures=flatten([[letter+'b',letter,letter+'#'] for letter in letter_range('a','h')])

#all common instruments - this can be a more inclusive list later
all_instruments= [string.lower() for string in[
    # Woodwinds
    "Flute", "Piccolo", "Clarinet", "Bass Clarinet", "Oboe", "English Horn", "Bassoon", "Contrabassoon", 
    "Soprano Saxophone", "Alto Saxophone", "Tenor Saxophone", "Baritone Saxophone",
    
    # Brass
    "Trumpet", "French Horn", "Trombone", "Bass Trombone", "Euphonium", "Tuba", "Cornet", "Flugelhorn","horn",
    
    # Percussion
    "Snare Drum", "Bass Drum", "Timpani", "Cymbals", "Glockenspiel", "Xylophone", "Marimba", "Vibraphone", 
    "Triangle", "Tambourine", "Wood Block", "Chimes", "Conga", "Bongo Drums",'bells',
    
    # Strings (Orchestra)
    "Violin", "Viola", "Cello", "Double Bass", "Harp",
    
    # Keyboard (Orchestra)
    "Piano", "Celesta",
    
    # Other Instruments (Orchestra)
    "Piccolo Trumpet", "Contrabass Clarinet", "Contrabass Trombone"
]]