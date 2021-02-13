import os
from PyPDF2 import PdfFileReader

dictionnaire_type = dict((('txt','text/plain'),('pdf','application/pdf'),('png','image/png'),('jpg','image/jpeg'),('jpeg','image/jpeg'),('gif','image/gif'),('doc','application/msword'),('docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document'),('csv','text/plain')))

def getFileMetasAndContent(file,mimetype):
    
    monContenu=""
    mesMetas = dict((("info1","info"),("info2",9)))

    if(mimetype == 'text/plain'):
        print()
    elif(mimetype == 'application/pdf'):
        print()
    elif(mimetype == 'image/jpeg'):
        print()
    elif(mimetype == 'image/gif'):
        print()
    elif(mimetype == 'image/gif'):
        print()
    elif(mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        print()
    

    return monContenu,mesMetas
