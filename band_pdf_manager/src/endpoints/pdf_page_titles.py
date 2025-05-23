import fitz
import easyocr
import helpers
import PIL
import numpy as np
import re
from PyPDF2 import PdfWriter, PdfReader
import os
import time

#generator function that returns all the images in a pdf file in numpy array format
def pdf_to_image(pdf_file):
    
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    # Count variable is to get the number of pages in the pdf
    for p in pdf_file:
        count += 1
    for i in range(count):
        val = f"image_{i+1}.png"
        page = pdf_file.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        #convert image to pil then to np array
        pix = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pix = np.array(pix)
        yield pix
    pdf_file.close()


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
    doc = fitz.open(pdf_file)
    images=[image for image in pdf_to_image(doc)]
    
    page_text=[image_to_text(image) for image in images[0:max_pages:1]]
    with open('log.txt','w+') as log:  
        log.write("\n".join(str(item) for item in page_text))


    page_instrument_references=text_to_instrument(page_text)
    
    instruments=[]
    prev_instrument=''
    for page in page_instrument_references:
        #number of instrument references on each page is the length of the page here
        if len(page)==1:
            instruments.append(page[0])
            prev_instrument=page[0]
        elif (len(page)==0):
            instruments.append(prev_instrument)
        elif len(page)>1:
            instruments.append(prev_instrument)
    
    
    return instruments


#return the instrument from each page of text
#takes a list of lists as input
#outputs a list of lists for each instrument referenced on each page
def text_to_instrument(page_text):
    page_instrument_references=[[] for page in page_text]
    for count,page in enumerate(page_text):
        if page!=[]:
            for text in page:

                for instrument in helpers.all_instruments:
                    if instrument in text.lower():

                        #eventually:
                            #use the text match so that we have the instrument part # (eg trumpet 2)
                            
                            #strip any number after a dash or slash - this keeps page numbering consistant:
                            #ie. trumpet 2-2 is the second page of trumpet 2 music, not a seperate instrument

                            #do not include periods in this list - Euphonium T.C and Euphonium B.C are seperate instruments

                        new_text=re.split(r'[-/()]', text)
                        if new_text!=[]:
                            new_text=new_text[0].strip()
                        else:
                            new_text=None
                        #only send the instrument for now - there's too many errors for instrument number etc.
                        page_instrument_references[count].append(instrument)
    return (page_instrument_references)

#get all indexes of the given item in a list
def get_indices(element, mylist):
    indices = []
    for i in range(len(mylist)):
        if mylist[i] == element:
            indices.append(i)
    return indices
def flatten(input_list):
    return([
    x
    for xs in input_list
    for x in xs
])

#turn a list of pages with elements into a list of page slices
#instrument list is a 1-d array of 1 instrument on each page
def instrument_pages_to_slices(instrument_list):
    instrument_set= set(instrument_list)
    slices=[]
    instruments=[]
    for instrument in instrument_set:
        indices = [index for index, element in enumerate(instrument_list) if element == instrument]
        print(indices) 
        first=min(indices)
        last=max(indices)
        instruments.append(instrument)
        slices.append(slice(first,last,1))
    return(instruments,slices)
    
    
    

#makes pdfs from lists of slices
#slices are the pages for each instrument
#instruments are the instruments for each slice
#pdf is the entire sheet score

#note-  fitz and pdfreader disagree on formats - this function only works with pdfreader

def pdf_splitter(slices,instruments,pdf):
    doc = PdfReader(pdf)

    for index,cur_slice in enumerate(slices):
        my_pages=[]
        for i in range(cur_slice.start,cur_slice.stop):
            new_page=doc.pages[i]
            my_pages.append(new_page)
        
        output = PdfWriter()
        for page in my_pages:
            output.add_page(page)
        name=pdf.split('.')[0]
        #use name as the folder for now, then put one file for each instrument
        if not os.path.exists(name):
            os.mkdir(name)

        with open(os.path.join(name,''.join([name+'_',"%s.pdf" % instruments[index]])), "wb") as outputStream:
            output.write(outputStream)

def end_to_end_pdf(pdf_file_name):

    instrument_list=(pdf_to_instruments(pdf_file_name))
    instruments,slices=instrument_pages_to_slices(instrument_list)
    #note-  fitz and pdfreader disagree on formats - this function only works with pdfreader
    doc = PdfReader(pdf_file_name)
    pdf_splitter(slices,instruments,pdf_file_name)



def test():
    text = [['Written in 2019 for the University of Wisconsin Stevens Point bands, Michael S Butler; director:', 'Dedicated to Donald E. Greene and in celebration of the 12Sth anniversary of UWSP', 'Trumpet in Bb 1', 'RIVER OF STARS', 'Barbara York', 'Allegro', '2', '72', '(to open)', '(solo)', '10', 'mute', 'm', 'Allegretto marcato', '112', 'Meno mosso', '24', '2', 'poco rit.', '3', '29', 'open', 'mp', '43', '55', '65', '73', 'Copyright 0 2019 Cimarron Music Press. All Rights Reserved.', 'www.CimarronMusiccom'],
     ['81', 'm', 'molto rit', '93', '=', '60', '167', '175', '101', '183', '76', '109', 'my]', 'rit.', '119| Allegro', '120', '(to mute)', '2', '/191', '60', 'm', '130', 'poco rit.', '96', '(solo)', 'mute', 'mp', 'poco meno mosso', '= 80', '98', '199|', '2091', '35', '(to open)', '138]', '= 76', 'rit', '3', '5', '218/', '148|', '=', '112', 'open', '158]', '(to mute)', 'mute', '6', 'm', 'mp', 'Trumpet in Bb 1 - 2', 'Trumpet in Bb 1 - 3'],
['Written in 2019 for the University of Wisconsin Stevens Point bands, Michael S Butler; director:', 'Dedicated to Donald E. Greene and in celebration of the 12Sth anniversary of UWSP', 'Trumpet in Bb 1', 'RIVER OF STARS', 'Barbara York', 'Allegro', '2', '72', '(to open)', '(solo)', '10', 'mute', 'm', 'Allegretto marcato', '112', 'Meno mosso', '24', '2', 'poco rit.', '3', '29', 'open', 'mp', '43', '55', '65', '73', 'Copyright 0 2019 Cimarron Music Press. All Rights Reserved.', 'www.CimarronMusiccom']]
    pdf_file_name='Hands of Mercy - Low Brass.pdf'    
    instrument_list=(pdf_to_instruments(pdf_file_name))
    instruments,slices=instrument_pages_to_slices(instrument_list)
    #note-  fitz and pdfreader disagree on formats - this function only works with pdfreader
    doc = PdfReader('Hands of Mercy - Low Brass.pdf')
    pdf_splitter(slices,instruments,pdf_file_name)

if __name__=='__main__':
    test()




