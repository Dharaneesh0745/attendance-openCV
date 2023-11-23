import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://face-attendance-cv-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')

data = {
    "01dj":
        {
            "name": "Dwayne Johnson",
            "major": "Mechanical",
            "starting_year": "2021",
            "total_attendance": 1,
            "gpa": "9.1",
            "year": "3",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "02ms":
        {
            "name": "Makato Shinkai",
            "major": "Arts",
            "starting_year": "2021",
            "total_attendance": 2,
            "gpa": "9.3",
            "year": "2",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "03or":
        {
            "name": "Olivia Rodrigo",
            "major": "Arts",
            "starting_year": "2022",
            "total_attendance": 3,
            "gpa": "8.6",
            "year": "1",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "04aa":
        {
            "name": "Afsal Ahmad",
            "major": "Machine Learning",
            "starting_year": "2022",
            "total_attendance": 4,
            "gpa": "8.4",
            "year": "1",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "05mrs":
        {
            "name": "Mugesh Ram Sundar",
            "major": "Machine Learning",
            "starting_year": "2022",
            "total_attendance": 1,
            "gpa": "8.4",
            "year": "1",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "06rc":
        {
            "name": "Ronnie Coleman",
            "major": "Ece",
            "starting_year": "2020",
            "total_attendance": 3,
            "gpa": "9.8",
            "year": "4",
            "last_attendance_time": "00:00:00 01-01-2023"
        },

    "07dh":
        {
            "name": "Dharaneesh",
            "major": "Machine Learning",
            "starting_year": "2022",
            "total_attendance": 1,
            "gpa": "9.0",
            "year": "1",
            "last_attendance_time": "00:00:00 01-01-2023"
        },
    "08sa":
        {
            "name": "Sanjeevi Kumar",
            "major": "Data Science",
            "starting_year": "2022",
            "total_attendance": 1,
            "gpa": "10.0",
            "year": "1",
            "last_attendance_time": "00:00:00 01-01-2023"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
