import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-cv-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-attendance-cv.appspot.com"
})

# import student images
folderPath = 'Faces'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return(encodeList)


print("Encoding ...")
encodeListKnown = findEncodings(imgList)
print("Encoding Successful")

encodeListWithIds = [encodeListKnown, studentIds]

file = open("Encode.p", 'wb')
pickle.dump(encodeListWithIds, file)
file.close()
print("File Saved")
