import numpy as np
import pandas as pd

np.random.seed(40)
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

from tf_keras_vis.gradcam import Gradcam
from tf_keras_vis.utils import normalize

import settings as st

from matplotlib import cm
import os
import cv2


class Predict:
    def __init__(self):
        self.n_step = 5
        self.generate_gradcam = False
        self.image_size = 384
        self.threshold = 0.5
        self.class_index = 0
        self.list_pos = [
            "safe_driving",
            "texting_R",
            "talking_to_the_phone_R",
            "texting_L",
            "talking_to_the_phone_L",
            "operating_the_radio",
            "drinking",
            "reaching_behind",
            "hair_and_makeup",
            "talking_to_passenger"
        ]

        self.normal_index = 0

    def predict(self, img_path, row, img=None, load=False, original_image_path=None, print_heatmap=False):
        if load == True:
            img = self.load_img(img_path)

        y_pred = self.calculate_score(img, original_image_path, self.n_step)

        if row is None:
            row = pd.Series()
            row['path'] = original_image_path
            row['results'] = {}
            row['labels'] = {}
            row['heatmap'] = ''

        i = 0
        for c in self.list_pos:
            if y_pred[i] > st.th[i]:
                label = c
                self.class_index = i
                row['results'] = {
                    'y_pred': y_pred[i],
                    'y_pred_nofinding': y_pred[self.normal_index],
                    'label': label
                }
            else:
                label = "no_" + c

            row['labels'][c] = {
                'y_pred': y_pred[i],
                'y_pred_nofinding': y_pred[self.normal_index],
                'label': label
            }
            i = i + 1

        if print_heatmap:
            print(y_pred)
            path_heatmap = self.grad_cam(im_path=img_path, original_image_path=original_image_path, img_input=img)
            row['heatmap'] = path_heatmap

        return row

    def normalize(self, image):
        image = (image - image.min())/(image.max() - image.min())
        return image

    def calculate_score(self, img, original_image_path, n_examples=5):
        y_pred = self.model.predict(img)
        y_pred = y_pred[0, :]
        # score = y_pred[self.class_index]
        return y_pred

    def load_img(self, img_path):
        imgs = np.array(
            [self.normalize(
                img_to_array(load_img(img_path, target_size=(self.image_size, self.image_size), color_mode='rgb')))])
        return imgs

    def grad_cam(self, im_path, original_image_path, img_input=None, positions=None):

        target = self.class_index

        if img_input is None:
            img_input = self.load_img(im_path)

        self.grad_func = Gradcam(self.model, self.model_modifier, clone=False)

        self.target = target
        cam = self.grad_func(self.loss, img_input, expand_cam=True)
        cam = normalize(cam)

        cam3 = np.uint8(cm.jet(cam[0])[..., :3] * 255) / 255

        img = cv2.imread(original_image_path)
        h, w, _ = img.shape
        img = img / 255

        filename, file_extension = os.path.splitext(original_image_path)
        filename = filename.split('/')[-1]

        th_color = 0.2
        cam3[np.where(cam[0] < th_color)] = 0

        cam3 = self.resize(cam3, h, positions, w)

        new_img = cam3 * 0.5 + img

        new_img = new_img / new_img.max()

        new_img_name = f"./heatmap/{filename}_activationmap_colors.png"

        plt.imsave(new_img_name, new_img)

        return new_img_name

    def resize(self, cam3, h, positions, w):
        if positions != None:
            x, y, xmax, ymax = positions
            cam3 = cv2.resize(cam3, ((xmax - x), (ymax - y)))
            cam_scaled = np.zeros((636, 636, 3))
            cam_scaled[y:ymax, x:xmax, :] = cam3
            cam3 = cam_scaled
            cam3 = cv2.resize(cam3, (w, h))
        else:
            cam3 = cv2.resize(cam3, (w, h))
        return cam3

    def model_modifier(self, m):
        m.layers[-1].activation = tf.keras.activations.linear
        return m

    def loss(self, output):
        output = output[0]
        return output[self.target]
