import os
import fileManager

# Fichier pour tester l'API à distance

#curl -F mydata=@mondoc.type http://127.0.0.1:5000/document

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/sample.pdf','application/pdf')

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/fichiertest.txt','text/plain')

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/Capture.PNG','image/png')

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/Canon_40D.jpg','image/jpeg')

print(metas)

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/oiseau.gif','image/gif')


contenu, metas = fileManager.getFileMetasAndContent('static/test-files/weather.csv','text/plain')

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/docxtest.docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document')

contenu, metas = fileManager.getFileMetasAndContent('static/test-files/ppttest.pptx','application/vnd.openxmlformats-officedocument.wordprocessingml.document')



