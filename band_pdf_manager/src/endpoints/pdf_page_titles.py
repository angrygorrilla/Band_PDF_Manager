import fitz
import easyocr
import helpers
import PIL
import numpy as np
import re
from PyPDF2 import PdfWriter, PdfReader


#generator function that returns all the images in a pdf file in numpy array format
def pdf_to_image(pdf_file):
    doc = fitz.open(pdf_file)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    # Count variable is to get the number of pages in the pdf
    for p in doc:
        count += 1
    for i in range(count):
        val = f"image_{i+1}.png"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        #convert image to pil then to np array
        pix = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pix = np.array(pix)
        yield pix
    doc.close()


#list slicer using slice objects
def select_portion(list_to_slice, slicer):
    return(list_to_slice[slicer])

#gather the text on one image in np array format
def image_to_text(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    return (result)


#collect the text from a set of pdf pages    
def pdf_to_instruments(pdf_file,max_pages=-1):

    images=[image for image in pdf_to_image(pdf_file)]
    
    page_text=[image_to_text(image) for image in images[0:max_pages:1]]
    with open('log.txt','w+') as log:  
        for item in page_text:
            if item is list:
                for str in item:
                    log.write(item)
            else:
                log.write(item)
    page_instrument_references=text_to_instrument(page_text)
    
    instruments=[]
    prev_instrument=''
    for page in page_instrument_references:
        if len(page)==1:
            instruments.append(page[0])
            prev_instrument=page[0]
        elif (len(page)==0):
            instruments.append(prev_instrument)
        elif len(page)>1:
            instruments.append(prev_instrument)
    
    
    return page_instrument_references


#return the instrument from each page of text
#takes a list of lists as input
#outputs a list of lists for each instrument referenced on each page
def text_to_instrument(page_text):
    page_instrument_references=[[] for page in page_text]
    for count,page in enumerate(page_text):
        if page!=[]:
            print('>page<')
            print(page)
            for text in page:

                for instrument in helpers.all_instruments:
                    if instrument in text.lower():
                        #use the text match so that we have the instrument part # (eg trumpet 2)
                        
                        #strip any number after a dash or slash - this keeps page numbering consistant:
                        #ie. trumpet 2-2 is the second page of trumpet 2 music, not a seperate instrument
                        new_text=re.split(r'[,-/()]', text)
                        if new_text!=[]:
                            new_text=new_text[0].strip()
                        else:
                            new_text=None
                        
                        page_instrument_references[count].append(new_text)
    return (page_instrument_references)

#get all indexes of the given item in a list
def get_indices(element, mylist):
    indices = []
    for i in range(len(mylist)):
        if mylist[i] == element:
            indices.append(i)
    return indices

#turn a list of pages with elements into a list of page slices
#instrument list is a 1-d array of 1 instrument on each page
def instrument_pages_to_slices(instrument_list):
    instrument_set= set(instrument_list)
    slices=[]
    instruments=[]
    for instrument in instrument_set:
        indices=get_indices(instrument,instrument_list)
        first=min(indices)
        last=max(indices)
        instruments.append(instrument)
        slices.append(slice(first,last,1))
    return(instruments,slices)
    
    
    

#makes pdfs from lists of slices
#slices are the pages for each instrument
#instruments are the instruments for each slice
#pdf is the entire sheet score
def pdf_splitter(slices,instruments,pdf):
    for index,cur_slice in enumerate(slices):
        pages=select_portion(pdf.pages,cur_slice)
        
    output = PdfWriter()
    output.add_page(pages)
    with open("document-page%s.pdf" % instruments[index], "wb") as outputStream:
        output.write(outputStream) 

def test():
    text = [['Written in 2019 for the University of Wisconsin Stevens Point bands, Michael S Butler; director:', 'Dedicated to Donald E. Greene and in celebration of the 12Sth anniversary of UWSP', 'Trumpet in Bb 1', 'RIVER OF STARS', 'Barbara York', 'Allegro', '2', '72', '(to open)', '(solo)', '10', 'mute', 'm', 'Allegretto marcato', '112', 'Meno mosso', '24', '2', 'poco rit.', '3', '29', 'open', 'mp', '43', '55', '65', '73', 'Copyright 0 2019 Cimarron Music Press. All Rights Reserved.', 'www.CimarronMusiccom'],
     ['81', 'm', 'molto rit', '93', '=', '60', '167', '175', '101', '183', '76', '109', 'my]', 'rit.', '119| Allegro', '120', '(to mute)', '2', '/191', '60', 'm', '130', 'poco rit.', '96', '(solo)', 'mute', 'mp', 'poco meno mosso', '= 80', '98', '199|', '2091', '35', '(to open)', '138]', '= 76', 'rit', '3', '5', '218/', '148|', '=', '112', 'open', '158]', '(to mute)', 'mute', '6', 'm', 'mp', 'Trumpet in Bb 1 - 2', 'Trumpet in Bb 1 - 3'],
['Written in 2019 for the University of Wisconsin Stevens Point bands, Michael S Butler; director:', 'Dedicated to Donald E. Greene and in celebration of the 12Sth anniversary of UWSP', 'Trumpet in Bb 1', 'RIVER OF STARS', 'Barbara York', 'Allegro', '2', '72', '(to open)', '(solo)', '10', 'mute', 'm', 'Allegretto marcato', '112', 'Meno mosso', '24', '2', 'poco rit.', '3', '29', 'open', 'mp', '43', '55', '65', '73', 'Copyright 0 2019 Cimarron Music Press. All Rights Reserved.', 'www.CimarronMusiccom']]
    pdf_file='Hands of Mercy - Low Brass.pdf'
    print(pdf_to_instruments(pdf_file),max_pages=2)


    #instruments=text_to_instrument(text)
    #instruments,slices=instrument_pages_to_slices(instruments[0])
    #print(slices)
    
test()




