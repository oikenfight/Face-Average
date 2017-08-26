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

import sys
import os
import dlib
import glob
from skimage import io

# if len(sys.argv) != 3:
#     print(
#         "Give the path to the trained shape predictor model as the first "
#         "argument and then the directory containing the facial men-faces.\n"
#         "For example, if you are in the python_examples folder then "
#         "execute this program by running:\n"
#         "    ./Face_Landmark_Detection.py shape_predictor_68_face_landmarks.dat ../examples/faces\n"
#         "You can download a trained facial shape predictor from:\n"
#         "    http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
#     exit()

# predictor_path = sys.argv[1]
# faces_folder_path = sys.argv[2]

# TODO: 今後変更する。faces_folder_path は DropBox から取ってくるようにする
predictor_path = './shape_predictor_68_face_landmarks.dat'
faces_folder_path = '../../FaceAverage/presidents_images/'
face_points_folder_path = '../../FaceAverage/presidents_points/'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
# win = dlib.image_window()

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):

    print("Processing file: {}".format(f))
    img = io.imread(f)

    # win.clear_overlay()
    # win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    if len(dets) >= 2:
        # 顔が 2 つ以上検出された場合、失敗する原因になるためはじく
        # TODO: あとで Exception 返すようにする
        # TODO: men-faces に対して数が合わなくなるとエラーになるため、その image を削除するようにする
        print('=======================================')
        print('error! found 2 more faces.')
        print('=======================================')
        continue

    # TODO: ファイルパスは DropBox とかに変更する
    # ファイルフルパスからフォルダパスと「.jpg」を取り除く
    face_file_name = f[(len(faces_folder_path)):-4]
    print(face_file_name)

    # 68 の点を書き込む txt ファイルを作成
    face_landmark_file = open(face_points_folder_path + face_file_name + '.txt', 'w')

    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))

        # ポイントをテキストファイルに書き込む
        print('===== ' + face_file_name + ' output ===============================')
        for i in xrange(68):
            # print(i)
            print(str(shape.part(i).x) + ' ' + str(shape.part(i).y))
            face_landmark_file.write(str(shape.part(i).x) + ' ' + str(shape.part(i).y) + '\n')

        print('===== output end ===============================')

        # Draw the face landmarks on the screen.
        # win.add_overlay(shape)

    # 書き込み終了
    face_landmark_file.close()

    # win.add_overlay(dets)
    # dlib.hit_enter_to_continue()
