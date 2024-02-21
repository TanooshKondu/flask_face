import os
import datetime
import cv2
from flask import Flask,jsonify,request,render_template

# AND INSTALL FACE RECOGNITION WITH
# pip install face_recognition
import face_recognition

app = Flask(_name_)

#CREATE VARIABLE REGISTER
registered_data = {}


@app.route("/")
def index():
    #NOW RENDER YOU HTML FILE
    return render_template("index.html")

# AND CREATE POST METHOD
@app.route("/register",methods=["POST"])
def register():
    name = request.form.get("name")
    #AND GET YOU PHOTO UPLOADS
    photo = request.files['photo']

    # AND NOW SAVE YOU PHOTO TO UPLOADS FOLDER
    # WHEN YOU register PROCESS
    uploads_folder = os.path.join(os.getcwd(),"static","uploads")
    # AND IF FOLDER UPLOADS NOT FOUND THIS SYSTEM WILL
    # AUTO CREATE FOLDER uploads
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    # AND SAVE YOU PHOTO IMAGE WITH FILE NAME DATE NOW
    photo.save(os.path.join(uploads_folder,f'{datetime.date.today()}_{name}.jpg'))
    
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"

    # AND SEND SUCCESS RESPOSE THEN PAGE WILL REFRESH AND LOGIN
    response = {"success":True,'name':name}
    return jsonify(response)


# AND NOW CREATE LOGIN route POST
@app.route("/login",methods=["POST"])
def login():
    photo = request.files['photo']

    # AND SAVE YOU photo  LOGIN TO FOLDER UPLOADS
    uploads_folder = os.path.join(os.getcwd(),"static","uploads")
    # AND CREATE FOLDER IF NOT FOUND
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    # AND SAVE FILE PHOTO LOGIN WITH YOU NAME
    login_filename = os.path.join(uploads_folder,"login_face.jpg")

    photo.save(login_filename)

    # AND THIS PROCESS WILL DETECT YOU CAMERA IS THERE FACE OR NOT
    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image,cv2.COLOR_BGR2GRAY)


    # AND LOAD YOU haar CASCADE FILE HERE
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image,scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

    # AND DETECT IF NO FACE IN CAMERA
    if len(faces) == 0:
        response = {"success": False}
        return jsonify(response)

    login_image = face_recognition.load_image_file(login_filename)
    # AND PROCESS ADNRECONITION YOU FACE

    # AND IF PHOTOS IN FOLDER UPLOADS FIND DOMINAN SIMILARITY
    # YOU IMAGES THEN LOGIN SUCCESS
    login_face_encodings = face_recognition.face_encodings(login_image)

    # AND PROCESS YOU LOGIN PHOTO WITH DIFFERENT PHOTO AFER REGISTER
    # wit face recognition
    for name,filename in registered_data.items():
        # FIND REGISTERED PHOTO
        # YOU UPLOADS FOLDER
        registered_photo = os.path.join(uploads_folder,filename)
        registered_image = face_recognition.load_image_file(registered_photo)

        face_face_encodings = face_recognition.face_encodings(registered_image)

        # AND COMPARE YOU IMAGE FROM LOGIN AND REGISTER PHOTO
        if len(registered_face_encodings) >0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_faces(registered_face_encodings,login_face_encodings[0])

            # AND SEE MATCHES
            print("matches",matches)
            if any(matches):
                response = {"success":True,"name":name}
                return jsonify(response)
    # AND IF NO MATCH FOUND
    response = {"success":False}
    return jsonify(response)

# AND THIS PAGE WILL SHOW SUCCESS PAGE IF YOU SUCCESS LOGIN
@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("success.html",user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True)
    