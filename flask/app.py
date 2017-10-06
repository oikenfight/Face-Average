# coding=utf-8

from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import json
from Face_Landmark_Detection import *
from FaceAverage import *
from ImageManager import ImageManager

app = Flask(__name__)


@app.route("/")
def index():
    image_manager = ImageManager()
    men_face_names = image_manager.all('men')
    women_face_names = image_manager.all('women')

    return render_template('index.html', men_face_names=men_face_names, women_face_names=women_face_names)


@app.route("/list_men")
def list_men():
    image_manager = ImageManager()
    men_face_names = image_manager.all('men')
    women_face_names = image_manager.all('women')

    return render_template('list_men.html', men_face_names=men_face_names, women_face_names=women_face_names)


@app.route("/list_women")
def list_women():
    image_manager = ImageManager()
    men_face_names = image_manager.all('men')
    women_face_names = image_manager.all('women')

    return render_template('list_women.html', men_face_names=men_face_names, women_face_names=women_face_names)


@app.route("/new_file")
def new_file():
    return render_template('new_file.html')


@app.route("/new_photo")
def new_photo():
    return render_template('new_photo.html')


@app.route("/mix")
def mix():
    image_manager = ImageManager()
    men_face_names = image_manager.all('men')
    women_face_names = image_manager.all('women')

    print(type(men_face_names))

    return render_template('mix.html', men_face_names=men_face_names, women_face_names=women_face_names)


@app.route("/upload_file", methods=['POST'])
def upload_file():
    # requested data
    img = request.files['face']
    gender = request.form['gender']

    print(img)

    # ImageManager
    image_manager = ImageManager()

    # make image name (str datetime)
    filename = image_manager.make_file_name()

    image_manager.upload(request.files['face'], gender, filename)

    # 検出が正しいか。正しい場合、./static/men-points/ txt ファイルが作成される
    detector = Detector(img, filename)
    try:
        detector.detect_landmark(gender)
    except Exception:
        print('exception in upload')
        # 作成されたファイルを削除しておく
        image_manager.remove(gender, filename)
        if os.path.isfile("./static/men-points" + filename + '.txt'):
            os.remove("./static/men-points" + filename + '.txt')
        print('clean up')
        # error
        return

    print('success')
    # success
    return jsonify({'status': 200})


@app.route("/upload_photo", methods=['POST'])
def upload_photo():
    print(request.form['face'])
    print(request.form['gender'])

    # requested data
    base64img = request.form['face']
    gender = request.form['gender']

    # ImageManager
    image_manager = ImageManager()

    # make image name (str datetime)
    filename = image_manager.make_file_name()

    # save image
    img = open('./static/' + gender + '-faces/' + filename + '.jpg', 'wb')
    img.write(base64img.decode('base64'))
    img.close()

    img = open('./static/' + gender + '-faces/' + filename + '.jpg', 'r')

    # 検出が正しいか。正しい場合、./static/men-points/ txt ファイルが作成される
    detector = Detector(img, filename)

    try:
        detector.detect_landmark(gender)
    except Exception:
        print('exception in upload')
        # 作成されたファイルを削除しておく
        image_manager.remove(gender, filename)
        if os.path.isfile("./static/men-points" + filename + '.txt'):
            os.remove("./static/men-points" + filename + '.txt')
        print('clean up')
        # error
        return

    img.close()
    print('success')
    # success
    return jsonify({'status': 200})


@app.route("/update")
def update():
    print('update')
    try:
        main('men')
        main('women')
    except:
        # error
        return
    # success
    return jsonify({'status': 200})


@app.route("/mix", methods=['POST'])
def original():
    men_selected = []
    women_selected = []

    if request.form['menSelected']:
        men_selected = request.form['menSelected'].split(',')
    if request.form['womenSelected']:
        women_selected = request.form['womenSelected'].split(',')

    try:
        custom(men_selected, women_selected)
    except Exception:
        # error
        print('error')
        return
    # success
    return jsonify({'status': 200})


@app.route("/webRTC")
def web_rtc():
    return render_template('webRTC.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
