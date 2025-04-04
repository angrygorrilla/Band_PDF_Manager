import fitz
import easyocr

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
        yield val
    doc.close()


def image_to_text(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    print(result)
    

pdf_file='River of Stars brass and percussion.pdf'
images=[image for image in pdf_to_image(pdf_file)]

text=[image_to_text(image) for image in images]
print(text)