import numpy as np

np.random.seed(40)
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

import settings as st

from predict import Predict


class ClassificationModel(Predict):
    def __init__(self):
        self.list_pos = [
            "safe driving",
            "texting - right",
            "talking to the phone - right",
            "texting - left",
            "talking on the phone - left",
            "operating the radio",
            "drinking",
            "reaching behind",
            "hair and makeup",
            "talking to passenger"
        ]

        self.image_size = 384
        self.generator = ImageDataGenerator(brightness_range=[0.7, 1.5],
                                            rotation_range=35,
                                            fill_mode='nearest',
                                            zoom_range=0.125,
                                            rescale=1. / 255)

        self.model = load_model(st.model_path)
        self.threshold = 0.5
        self.n_step = 5
        self.normal_index = 0