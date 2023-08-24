import cv2
import os
import pickle
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-cv-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-attendance-cv.appspot.com"
})
bucket = storage.bucket()

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

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    # img = cv2.flip(img, 1)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # img = cv2.flip(img, 1)

    imgBackGround[162:162 + 480, 55:55 + 640] = img
    imgBackGround[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

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
            # imgBackGround = cvzone.cornerRect(imgBackGround, bbox, rt=0)
            id = studentIds[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:

        if counter == 1:

            # Getting Data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            # Getting image
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackGround, str(studentInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackGround, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackGround, str(studentInfo['gpa']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackGround, str(studentInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackGround, str(studentInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1),
        cv2.putText(imgBackGround, str(studentInfo['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        (w, h), bs = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackGround, str(studentInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackGround[175:175+216, 909:909+216] = imgStudent

        counter += 1

    # cv2.imshow("Face Cam", img)
    cv2.imshow("Attendance ", imgBackGround)
    cv2.waitKey(1)

