from tableofContentLink import tocLink
from helperFunctions import addHeaders, pdfConversion, pdfCombined, tableOfContentGenerator, deleteProcessFiles
from SnowflakeConnector import extractDataFromSnowflake
from individualTableProcessor import tableProcessor
import os
import time

print("WELCOME TO CEA DATABASE TABLE DICTIONARY GENERATOR!")
print("Deleting Ditionary.pdf (if existed)...")
if(os.path.isfile("Dictionary.pdf") ):
  os.remove("Dictionary.pdf")
deleteProcessFiles()
extractedData= extractDataFromSnowflake()
dfs=extractedData[0]
tableNameAndComment = extractedData[1]
viewNameAndComment = extractedData[2]


tablesProcessedInfo= tableProcessor(dfs,tableNameAndComment,viewNameAndComment)
tableOfContentList=tablesProcessedInfo[0]
pdfList=tablesProcessedInfo[1]
tableNameList=tablesProcessedInfo[2]

tableOfContentGenerator(tableOfContentList)

pdfConversion("processFiles\\table_of_content_temp.html","processFiles\\table_of_content_temp.pdf")
addHeaders ("processFiles\\table_of_content_temp.pdf","processFiles\\table_of_content.pdf",2, "NA","NA",False,0)

pdfCombined("processFiles\\table_of_content.pdf",pdfList,tableNameList)

tocLink("processFiles\\dictionary.pdf")

deleteProcessFiles()
print("Dictionary - Successfully Generated! :D")
print("Have a great day!")
