#!/usr/bin/python
# coding=utf-8
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example program shows how to find frontal human faces in an image and
#   estimate their pose.  The pose takes the form of 68 landmarks.  These are
#   men-points on the face such as the corners of the mouth, along the eyebrows, on
#   the eyes, and so forth.
#
#   This face detector is made using the classic Histogram of Oriented
#   Gradients (HOG) feature combined with a linear classifier, an image pyramid,
#   and sliding window detection scheme.  The pose estimator was created by
#   using dlib's implementation of the paper:
#      One Millisecond Face Alignment with an Ensemble of Regression Trees by
#      Vahid Kazemi and Josephine Sullivan, CVPR 2014
#   and was trained on the iBUG 300-W face landmark dataset.
#
#   Also, note that you can train your own models using dlib's machine learning
#   tools. See train_shape_predictor.py to see an example.
#
#   You can get the shape_predictor_68_face_landmarks.dat file from:
#   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#   or
#       python setup.py install --yes USE_AVX_INSTRUCTIONS
#   if you have a CPU that supports AVX instructions, since this makes some
#   things run faster.  
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake and boost-python installed.  On Ubuntu, this can be done easily by
#   running the command:
#       sudo apt-get install libboost-python-dev cmake
#
#   Also note that this example requires scikit-image which can be installed
#   via the command:
#       pip install scikit-image
#   Or downloaded from http://scikit-image.org/download.html. 

import dlib
from skimage import io


class Detector:
    PREDICTOR_PATH = './shape_predictor_68_face_landmarks.dat'
    MEN_FACES_FOLDER_PATH = './static/men-faces/'
    WOMEN_FACES_FOLDER_PATH = './static/women-faces/'
    MEN_POINTS_FOLDER_PATH = './static/men-points/'
    WOMEN_POINTS_FOLDER_PATH = './static/women-points/'

    def __init__(self, img, name):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.PREDICTOR_PATH)
        self.img = img
        self.name = name

    def get_path(self, gender):
        if gender == 'men':
            face_path = self.MEN_FACES_FOLDER_PATH
            points_path = self.MEN_POINTS_FOLDER_PATH
        else:
            face_path = self.WOMEN_FACES_FOLDER_PATH
            points_path = self.WOMEN_POINTS_FOLDER_PATH

        return face_path, points_path

    def detect_landmark(self, gender):
        face_path, points_path = self.get_path(gender)

        img = io.imread(self.img)

        dets = self.detector(img, 1)

        # 顔が 2 つ以上検出された場合、失敗する原因になるためはじく
        if len(dets) != 1:
            print('==================================')
            print('error! detected multiple faces')
            print('==================================')
            raise Exception

        try:
            # 68 の点を書き込む txt ファイルを作成
            face_landmark_file = open(points_path + self.name + '.txt', 'w')

            # 68個のポイントを求める
            shape = self.predictor(img, dets[0])

            # ポイントをテキストファイルに書き込む
            for i in xrange(68):
                face_landmark_file.write(str(shape.part(i).x) + ' ' + str(shape.part(i).y) + '\n')

            # 書き込み終了
            face_landmark_file.close()
        except:
            raise Exception

        return True

