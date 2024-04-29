import pyrebase

firebaseConfig = {
        'apiKey': "AIzaSyCmH1QKp1t4y_gsNJ-63_NbsRHGlWuxGy0",
        'authDomain': "apartments-8578b.firebaseapp.com",
        'projectId': "apartments-8578b",
        'storageBucket': "apartments-8578b.appspot.com",
        'messagingSenderId': "412201567680",
        'appId': "1:412201567680:web:f53080566635a954187425",
        'measurementId': "G-VR2EDWMR3X",
        'databaseURL':''
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

email = 'test2@gmail.com'
password = '123456'

# user = auth.create_user_with_email_and_password(email,password)
# print(user)

user = auth.sign_in_with_email_and_password(email,password)
info = auth.get_account_info(user['idToken'])
print(info)