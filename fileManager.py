import os, time
from PyPDF2 import PdfFileReader
from PIL import Image
from PIL.ExifTags import TAGS
import base64
import textract


dictionnaire_type = dict((('txt','text/plain'),('pdf','application/pdf'),('png','image/png'),('jpg','image/jpeg'),('jpeg','image/jpeg'),('gif','image/gif'),('docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document'),('pptx','application/vnd.openxmlformats-officedocument.presentationml.presentation'),('csv','text/plain')))

def getFileMetasAndContent(file,mimetype):
    
    monContenu=""
    mesMetas = dict()
    mesMetas["last_modified_date"] = time.ctime(os.path.getmtime(file))
    mesMetas["creation_date"] = time.ctime(os.path.getctime(file))

    if(mimetype == 'text/plain'):
        with open(file) as f:
            i = 0
            for line in f:
                monContenu += line.strip()
                i+= 1
            mesMetas["nomber_of_caraters"] = len(monContenu)
            mesMetas["nomber_of_lignes"] = i

    elif(mimetype == 'application/pdf'):
        with open(file, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()
            mesMetas["number_of_pages"]=number_of_pages

            for page in range(number_of_pages):
                monContenu += pdf.getPage(page).extractText()

        mesMetas["author"] = info.author
        mesMetas["creator"] = info.creator
        mesMetas["producer"] = info.producer
        mesMetas["subject"] = info.subject
        mesMetas["title"] = info.title

    elif(mimetype == 'image/jpeg'):
        fullDico = getAllInfo(file)
        mesMetas["size"] = fullDico["_size"]

        try:
            mesMetas["mode"] = fullDico["mode"]
        except KeyError:
            print("clef absente : mode")
        try:
            mesMetas["dpi"] = fullDico["info"]["dpi"]
        except KeyError:
            print("clef absente : dpi")

        monContenu = encodeImage(file).decode('utf-8')

    elif(mimetype == 'image/gif'):
        fullDico = getAllInfo(file)
        mesMetas["size"] = fullDico["_size"]
        try:
            mesMetas["mode"] = fullDico["mode"]
        except KeyError:
            print("clef absente : mode")
        mesMetas["duration"] = fullDico["info"]["duration"]
        monContenu = encodeImage(file).decode('utf-8')
    elif(mimetype == 'image/png'):
        fullDico = getAllInfo(file)
        mesMetas["size"] = fullDico["_size"]
        try:
            mesMetas["mode"] = fullDico["mode"]
        except KeyError:
            print("clef absente : mode")
        try:
            mesMetas["dpi"] = fullDico["info"]["dpi"]
        except KeyError:
            print("clef absente : dpi")
        monContenu = encodeImage(file).decode('utf-8')
    elif(mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        monContenu = textract.process(file).decode('utf-8')
    elif(mimetype == 'application/vnd.openxmlformats-officedocument.presentationml.presentation'):
        monContenu = textract.process(file).decode('utf-8')
    return monContenu,mesMetas

def getAllInfo(image):
    im = Image.open(image)
    #renvoie toutes les informations relatives a l'image
    #utilise dan le projet pour stocker les meta datas
    return im.__dict__

def encodeImage(file):
    encoded_string = ""
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string