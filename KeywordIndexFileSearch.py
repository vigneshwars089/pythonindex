class index:
    #Definition for Indexing Txt files
    def indextxt(self,search_path,fname,search_str):
        result1="result1"
        fo = open(search_path+fname)
        # Read the first line from the file
        line = fo.readline()
        # Initialize counter for line number
        line_no = 1
        # Loop until EOF
        while line != '' :
            # Search for string in line
            index = line.find(search_str)
            if ( index != -1) :
                res=str("Found in : " + str(fname) + "[Line no - " + str(line_no) + ", Char Indx - " + str(index) + "] ")
                result1=res+result1
            # Read next line
            line = fo.readline()  
            # Increment line counter
            line_no += 1
        # Close the files
        fo.close()
        return(result1)
         
    #Definition for Indexing PDF files
    def indexpdf(self,filename,search_str):
            result2="result2"
            filename=fname  
            #print(filename)
            pdfFileObj=open(filename,mode='rb')
            #print("in")
            pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
            number_of_pages=pdfReader.numPages
            
            #for word in searchwords:
            for page in range(number_of_pages):
                pages_text=pdfReader.getPage(page).extractText().split('\n')
                line_no = 1
                for line in pages_text:
                    if(re.search(search_str,line)):
                        res=str("Found in File - "+ str(filename) +" , Page no - " + str(page) + ", Line no - " + str(line_no) + ", Line - [ "+str(line)+ " ]] ")
                        result2=res+result2
                    line_no += 1
            return(result2)        
                 
    #Definition for extracting text from Docx files
    def indexDocs(self,path,search_str):
        """
        Take the path of a docx file as argument, return the text
        """
        result3="result3"
        document = zipfile.ZipFile(path)
        #contentToRead = ["header2.xml", "document.xml", "footer2.xml"]
        contentToRead = ["document.xml"]
        paragraphs = []
    
        for xmlfile in contentToRead:
            xml_content = document.read('word/{}'.format(xmlfile))
            tree = XML(xml_content)
            for paragraph in tree.getiterator(PARA):
                texts = [node.text
                         for node in paragraph.getiterator(TEXT)
                         if node.text]
                if texts:
                    textData = ''.join(texts)
                    if xmlfile == "footer2.xml":
                        extractedTxt = "Footer : " + textData
                    elif xmlfile == "header2.xml":
                        extractedTxt = "Header : " + textData
                    else:
                        extractedTxt = textData
    
                    paragraphs.append(extractedTxt)
        document.close()
        line_no = 1
        for line in paragraphs:
            if search_str in line: 
                 res=str("Found in : " + str(fname) + "[Paragraph no - " + str(line_no) + "] ")
                 result3=res+result3
            line_no += 1
        return(result3)         
  
#Import all required modules
def mainfun(search_str):
    import sys
    sys.path.append(r"C:\Program Files\Anaconda3\Lib")
    #sys.path.append(r"C:\Program Files\Anaconda3\Lib")
    import os
    import PyPDF2
    import re
    import zipfile 
    
    try:
        from xml.etree.cElementTree import XML
    except ImportError:
        from xml.etree.ElementTree import XML
    output="output"
    #global variables for word document extraction
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    # Ask the user to enter string to search
    #search_path = input("Enter directory path to search : ")
    search_path="D:\pythonlucene\txt"
    #search_str = input("Enter the search string : ")
    
    # Append a directory separator if not already present
    if not (search_path.endswith("/") or search_path.endswith("\\") ): 
        search_path = search_path + "/"
                                                              
    # If path does not exist, set search path to current directory
    if not os.path.exists(search_path):
        search_path ="."
        
    #Create object for class    
    ind=index()
    
    # Repeat for each file in the directory  
    for fname in os.listdir(search_path):
        # Apply file type filter   
        if fname.endswith(".txt"):
            out=ind.indextxt(search_path,fname,search_str)
            output=out+output
        elif fname.endswith(".pdf"):
            out=ind.indexpdf(fname,search_str)
            output=out+output
        elif (fname.endswith(".docx") or fname.endswith(".doc")):
            doctext=[]
            out=ind.indexDocs(fname,search_str)
            output=out+output
    return(output)    