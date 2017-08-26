# coding=utf-8

from datetime import datetime, timedelta, tzinfo
import glob
from skimage import io
import os


class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'JST'


class ImageManager:
    MEN_FACES_FOLDER_PATH = './static/men-faces/'
    WOMEN_FACES_FOLDER_PATH = './static/women-faces/'
    MEN_POINTS_FOLDER_PATH = './static/men-points/'
    WOMEN_POINTS_FOLDER_PATH = './static/women-points/'

    def __init__(self):
        pass

    def make_file_name(self):
        now = datetime.now(tz=JST())
        str = now.strftime('%Y-%m-%d_%H-%M-%S')
        return str

    def get_path(self, gender):
        if gender == 'men':
            face_path = self.MEN_FACES_FOLDER_PATH
            points_path = self.MEN_POINTS_FOLDER_PATH
        else:
            face_path = self.WOMEN_FACES_FOLDER_PATH
            points_path = self.WOMEN_POINTS_FOLDER_PATH

        return face_path, points_path

    # 画像一覧を取得する
    def all(self, gender):
        face_path, points_path = self.get_path(gender)

        image_names = []

        for f in glob.glob(os.path.join(face_path, "*.jpg")):
            img = io.imread(f)

            # ファイルフルパスからフォルダパスと「.jpg」を取り除く
            img_name = f[(len(face_path)):-4]

            # txt ファイルが見つかるかチェック
            if os.path.isfile(points_path + img_name + '.txt'):
                image_names.append(img_name)

        return image_names

    # 画像を保存する
    def upload(self, img, gender, filename):
        face_path, points_path = self.get_path(gender)

        img.save(face_path + filename + '.jpg')
        return

    # 画像を削除する
    def remove(self, gender, filename):
        face_path, points_path = self.get_path(gender)

        os.remove(face_path + filename + '.jpg')
        return
