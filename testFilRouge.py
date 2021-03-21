import os
import requests

#Méthode pour renouveller le token OAuth2 auprès de WSO2
def renewToken():
    url = 'https://filrougewso2.spo.p2021.ajoga.fr:8243/token'
    headers = {'Authorization': 'Basic V3FCU25OX01seUFmV21DNnBOSGQ1UmdsQVhzYTpYcmRwNU1talFfMkhWM0FiRkZpQTFXMV9zZWth'}
    r = requests.post(url, data={'grant_type':'password','username':'filrougeuser','password':'filrougeuser'}, headers=headers, verify=False)
    return r

#Méthode pour uploader via WSO2 avec un token valide
def test_uploadImage_wso2(token):
    url = 'https://filrougewso2.spo.p2021.ajoga.fr:8243/filrouge/1.0.0/document'
    headers = {'Authorization':'Bearer '+token}
    fichierToUpload = {'mydata' : open('./static/test-files/Capture.PNG','rb')}
    r = requests.post(url, headers=headers, verify=False, files=fichierToUpload)
    return r

#Méthode pour uploader un fichier en accédant directement à l'application
def test_uploadImage_without_wso2():
    url = 'https://filrougev3.spo.p2021.ajoga.fr/document'
    fichierToUpload = {'mydata' : open('./static/test-files/Capture.PNG','rb')}
    r = requests.post(url, files=fichierToUpload)
    return r

response = test_uploadImage_without_wso2()
print(response.json()['message'])

token = renewToken().json()['access_token']
reponse_2 = test_uploadImage_wso2(token)
print(reponse_2.json()['message'])