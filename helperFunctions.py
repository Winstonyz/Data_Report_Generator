from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyQt5.QtWidgets import QApplication
import sys
import os, shutil
from reportlab.lib.utils import ImageReader


#function to break comments into multiple lines so that they be properly displayed in the pdf files
def breakText(text):
    print("Enter helperFunctions/breakText function...")
    textBreak=[]
    if(text.count(" ")<=7 and len(text)<=35):
        textBreak.append(text)
        print("COMPLETED: helperFunctions/breakText")
        return textBreak
    else:
        breakCount=0
        breakLimit=text.count(" ")//7
        textLength=len(text)
        while (breakCount<breakLimit or textLength>=35):
            portion=" ".join(text.split(" ", 7)[:7])
            portionLength=len(portion)
            breakNumber=7
            while(portionLength>35):
                breakNumber = breakNumber-1
                portion=" ".join(text.split(" ", breakNumber)[:breakNumber])
                portionLength=len(portion)
                
            textBreak.append(portion)
            nextPortion= text.split(" ", breakNumber)
            text=nextPortion[breakNumber]
            breakCount=breakCount+1
            textLength=len(text)

        textBreak.append(text)
        print("COMPLETED: helperFunctions/breakText")
        return(textBreak)

#function to add dictionary texts (headers, titles and all info other than the table/view columns info)
def addHeaders (filename,newFileName,tableIndex, structureName,comment,tbcSetup, pageNumber):
    print("Enter helperFunctions/addHeaders function...")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica-Bold', 15)
    can.drawString(150, 795, "CLEAN ENERGY ASSOCIATES DATA DICTIONARY")
    
    #comment = breakText("We observe today not a victory of party but a celebration of freedom--symbolizing an end as well as a beginning--signifying renewal as well as change. For I have sworn before you and Almighty God the same solemn oath our forbears prescribed nearly a century and three-quarters ago.")
    splitComment = breakText(comment)
    #texts for all pages other than the table of content
    logo = ImageReader("""
            https://images.squarespace-cdn.com/content/v1/5ea2eb4be710ac685db45b46/e646ea87-9364-43ca-8ba6-7687860b6a37/Official+CEA+Logo+-+Transparent.png
            """)
    can.drawImage(logo, 20, 800, width=70, height=23, mask='auto')
    
    if tbcSetup:
        can.setFont('Helvetica', 8)
        can.drawString(255, 785, "[Click here for the Table of Content]")

        if(structureName.startswith('V_')):
            can.setFont('Helvetica-Bold', 10)
            can.drawString(100, 765, "View Index:")
            can.drawString(100, 755, "View Name: ")
            can.drawString(400, 735, "View Comment:")
            can.drawString(100, 745, "View Columns:")

            can.setFont('Helvetica', 9)
            can.drawString(160, 765, "0"+str(tableIndex))
            can.drawString(160, 755, structureName)

        else:
            can.setFont('Helvetica-Bold', 10)
            can.drawString(100, 765, "Table Index:")
            can.drawString(100, 755, "Table Name: ")
            can.drawString(400, 735, "Table Comment:")
            can.drawString(100, 745, "Table Columns:")

            can.setFont('Helvetica', 9)
            can.drawString(160, 765, "0"+str(tableIndex))
            can.drawString(160, 755, structureName)
            can.drawString(390, 725, comment)
        
        commentBoxHeight=725
        for i in splitComment:
            #print (i)
            can.drawString(400, commentBoxHeight, i)
            commentBoxHeight = commentBoxHeight-10
        can.setFont('Helvetica', 10)
        can.drawString(275, 70, "Page: "+str(pageNumber))

    #text for the first page (table of content)
    else:
        can.setFont('Helvetica', 10)
        can.drawString(215, 765, "[Every line under \"TABLE OF CONTENTS\" is clickable]")
    
    #cover all original page numbers ("1" for every page)
    can.setFillColor("white")
    can.roundRect(475, 82, 25, 12, 4, stroke=0, fill=1)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(newFileName, "wb")
    output.write(outputStream)
    outputStream.close()
    print("COMPLETED: helperFunctions/addHeaders function")



#convert html files (which contain all the column info tables) into pdf files
def pdfConversion(filename,pdfName):
    print("Enter helperFunctions/pdfConversion function...")
    app = QApplication(sys.argv)
    doc = QTextDocument()
    location = filename
    html = open(location).read()
    doc.setHtml(html)

    printer = QPrinter()
    printer.setOutputFileName(pdfName)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageSize(QPrinter.A4)
    printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter)

    doc.print_(printer)
    print("COMPLETED: helperFunctions/pdfConversion function")


#combine Table of Content page as well as all individual dictionary page
def pdfCombined(toc,pdfs, tableNames):
    print("Enter helperFunctions/pdfCombined function...")
    merger = PdfFileMerger()
    merger.append(toc)
    count=1
    i=0
    for pdf in pdfs:
        merger.append(pdf)
        merger.addBookmark(tableNames[i],count,parent=None)
        i=i+1
        count=count+1

    merger.write("processFiles\\dictionary.pdf")
    merger.close()
    print("COMPLETED: helperFunctions/pdfCombined function")


#generate the table of content (html format)
def tableOfContentGenerator(tableOfContentList):
    print("Enter helperFunctions/tableOfContentGenerator function...")
    tocText = '''
    <html>
        <body>
    '''
    tocText2 = '''
        </body>
    </html>
    '''

    tocText=tocText+tableOfContentList+tocText2

    file = open("processFiles\\table_of_content_temp.html","w")
    file.write(tocText)
    file.close()
    print("COMPLETED: helperFunctions/tableOfContentGenerator function")

#automatically delete all files in the processFiles folder
def deleteProcessFiles():
    print("Deleting existing files (if any) in processFiles folder...")
    folder = 'processFiles'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
