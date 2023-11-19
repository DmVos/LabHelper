
from keras.src.mixed_precision.loss_scale_optimizer import optimizer
from keras.api._v2.keras import activations
from keras.models import load_model
import os

import numpy as np
import tensorflow as tf




def image_classification(image_input):
    class_names = ['5', '6', '7', '8', '9']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "corr_model_01_11.h5")
    model = load_model(model_path)


# load image
    img_array = tf.keras.utils.img_to_array(image_input)
    img_array = tf.expand_dims(img_array, 0)

# make predictions
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

# print inference result
    return ("На изображении скорее всего {} ({:.2f}% вероятность)".format(class_names[np.argmax(score)],100 * np.max(score)))
