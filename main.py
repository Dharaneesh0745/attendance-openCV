import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone

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

    # img = cv2.flip(img, 1)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # img = cv2.flip(img, 1)

    imgBackGround[162:162 + 480, 55:55 + 640] = img
    imgBackGround[44:44 + 633, 808:808 + 414] = imgModeList[3]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeFace, encodeListKnown)
        faceDis = face_recognition.face_distance(encodeFace, encodeListKnown)
        print("matches : ", matches)
        print("Dis : ", faceDis) 

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackGround = cvzone.cornerRect(imgBackGround, bbox, rt=0)

    # cv2.imshow("Face Cam", img)
    cv2.imshow("Attendance ", imgBackGround)
    cv2.waitKey(1)
