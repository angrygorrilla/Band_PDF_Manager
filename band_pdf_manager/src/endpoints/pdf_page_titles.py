import fitz
import easyocr
import helpers
import PIL
import numpy as np

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


def image_to_text(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    return (result)
    
def pdf_to_instruments(pdf_file,max_pages=-1):

    images=[image for image in pdf_to_image(pdf_file)]
    page_text=[image_to_text(image) for image in images[0:max_pages:1]]
    page_instrument_references=[[] for item in page_text[0:max_pages:1]]
    print(page_text)
    for count,page in enumerate(page_text):
        if page!=[]:
            print('>page<')
            print(page)
            for text in page:
                print(">text<")
                print (text)
                for instrument in helpers.all_instruments:
                    if instrument in text.lower():
                        #use the text match so that we have the instrument part # (eg trumpet 2)
                        page_instrument_references[count].append(text)
    return page_instrument_references


def test():
   instruments=pdf_to_instruments('River of Stars brass and percussion.pdf',max_pages=2)
   print(instruments)
test()




