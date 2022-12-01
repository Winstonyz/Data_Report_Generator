from helperFunctions import addHeaders, pdfConversion

#function to turn each table/view extracted from the Snowflake database into a pdf file
def tableProcessor(dfs,tableNameAndComment, viewNameAndComment):
  print("Enter individualTableProcessor/tableProcessor function...")
  count=0
  pdfList=[]
  tableNameList=[]
  tocString="       <h1>TABLE OF CONTENT</h1> \n"
  tableCounter=1
  viewCounter=1
  for i in dfs:
      print("Processing table/view No."+str(count+1)+": "+i)
      table = dfs[i]
      if(i.startswith('V_')):
          tableFullListName="View "+str(viewCounter)+": "+ i
      else:
          tableFullListName="Table "+str(tableCounter)+": "+ i
      tocNew="         <p>"+tableFullListName+"</p> \n"
      tocString=tocString+tocNew
      table=table.drop(['TABLE_NAME'], axis=1)
      table=table.reset_index(drop=True)
      tableNameList.append(i)

      filename= 'processFiles\\'+str(count)+'.html'
      
      pdfFileName='processFiles\\'+str(count)+'.pdf'
      table.to_html(filename)

      pdfConversion(filename,pdfFileName)

      newFileName='processFiles\\'+"0"+str(count)+'.pdf'

      tableOrViewComment="comment"

      if(i.startswith('V_')):
        #add view comments
        for oneView in viewNameAndComment:
            if oneView==i:
                tableOrViewComment = viewNameAndComment[oneView]
        pageNumber=count+1
        addHeaders(pdfFileName,newFileName, viewCounter, i, tableOrViewComment, True, pageNumber)
        pdfList.append(newFileName)
        viewCounter=viewCounter+1

      else:
        for oneTable in tableNameAndComment:
            if oneTable==i:
                tableOrViewComment = tableNameAndComment[oneTable]
        #add table comments
        pageNumber=count+1
        addHeaders(pdfFileName,newFileName, tableCounter, i, tableOrViewComment, True, pageNumber)
        pdfList.append(newFileName)
        
        tableCounter=tableCounter+1

      count=count+1

  print("COMPLETED: individualTableProcessor/tableProcessor function")
  return tocString,pdfList,tableNameList
  