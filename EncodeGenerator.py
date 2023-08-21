import cv2
import face_recognition
import pickle
import os

# import student images
folderPath = 'Faces'
PathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
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
