import pyrebase

firebaseConfig = {
        'apiKey': "AIzaSyCmH1QKp1t4y_gsNJ-63_NbsRHGlWuxGy0",
        'authDomain': "apartments-8578b.firebaseapp.com",
        'projectId': "apartments-8578b",
        'storageBucket': "apartments-8578b.appspot.com",
        'messagingSenderId': "412201567680",
        'appId': "1:412201567680:web:f53080566635a954187425",
        'measurementId': "G-VR2EDWMR3X",
        'databaseURL':'https://apartments-8578b-default-rtdb.firebaseio.com/'
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def get_name(username):
    info =(db.child("users").child(username).child("name").get())
    return info.val()

