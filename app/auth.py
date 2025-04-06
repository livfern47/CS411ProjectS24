import pyrebase
# Read secret information from ignored file
keys = open("key.txt")

# FIREBASE SETUP
config = {
        'apiKey': keys.readline(),
        'authDomain': keys.readline(),
        'projectId': keys.readline(),
        'storageBucket':  keys.readline(),
        'messagingSenderId':  keys.readline(),
        'appId':  keys.readline(),
        'measurementId':  keys.readline(),
        'databaseURL': keys.readline(),
}
keys.close()

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


def get_name(username):
    info =(db.child("users").child(username).child("name").get())
    return info.val()

