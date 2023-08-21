import cv2
import os
import pickle

import face_recognition

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackGround = cv2.imread('Resources/background.png')

# importing images into a List

folderModePath = 'Resources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for modes in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, modes)))

# cv2.imshow("YO", imgModeList[0])

# Load the encoded file

print("Loading Encoded File ...")
file = open('Encode.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
file.close()
print("Loading Complete")

while True:
    success, img = cap.read()

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

    # img = cv2.flip(img, 1)

    imgBackGround[162:162 + 480, 55:55 + 640] = img
    imgBackGround[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeFace, encodeListKnown)
        faceDis = face_recognition.face_distance(encodeFace, encodeListKnown)
        print("matches : ", matches)
        print("Dis : ", faceDis)

    # cv2.imshow("Face Cam", img)
    cv2.imshow("Attendance ", imgBackGround)
    cv2.waitKey(1)
