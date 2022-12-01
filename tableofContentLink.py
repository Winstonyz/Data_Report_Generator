from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path

#add inner-pdf links to the Table of Content page
def tocLink(dictionaryfile):
    print("Enter tableofContentLink/tocLink function...")
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(open(dictionaryfile,'rb'))
    # add each page in pdf to pdf writer
    num_of_pages = pdf_reader.getNumPages()

    for page in range(num_of_pages):
        current_page = pdf_reader.getPage(page)
        pdf_writer.addPage(current_page)

    # Add Links
    i=0
    pageGoal=1
    pageNum1=704
    pageNum2=719
    print(num_of_pages)
    while i<num_of_pages-1:
        pdf_writer.addLink(
            pagenum=0, # index of the page on which to place the link
            pagedest=pageGoal, # index of the page to which the link should go
            rect=RectangleObject([90,pageNum1,260,pageNum2]), # clickable area x1, y1, x2, y2 (starts bottom left corner)
        )
        pageGoal=pageGoal+1
        pageNum1=pageNum1-15
        pageNum2=pageNum2-15

        if(i!=0):
            pdf_writer.addLink(
                pagenum=i, # index of the page on which to place the link
                pagedest=0, # index of the page to which the link should go
                rect=RectangleObject([248,780,390,795]), # clickable area x1, y1, x2, y2 (starts bottom left corner)

            )
        i=i+1

    pdf_writer.addLink(
        pagenum=num_of_pages-1, # index of the page on which to place the link
        pagedest=0, # index of the page to which the link should go
        rect=RectangleObject([248,780,390,795]), # clickable area x1, y1, x2, y2 (starts bottom left corner)
        )
        
    with open(path.abspath('Dictionary.pdf'), 'wb') as link_pdf:
        pdf_writer.write(link_pdf)

    print("COMPLETED: tableofContentLink/tocLink function")
