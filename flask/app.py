# coding=utf-8

from flask import Flask, render_template, request
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


@app.route("/upload", methods=['POST'])
def upload():
    # requested data
    img = request.files['face']
    gender = request.form['gender']

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

    # success
    return ""


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
    return ""


@app.route("/original", methods=['POST'])
def original():
    men_selected = []
    women_selected = []

    if request.form['menSelected']:
        men_selected = request.form['menSelected'].split(',')
    if request.form['womenSelected']:
        women_selected = request.form['womenSelected'].split(',')

    try:
        custom(men_selected, women_selected)
    except:
        # error
        return
    # success
    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
