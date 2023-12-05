from keras.src.mixed_precision.loss_scale_optimizer import optimizer
from keras.api._v2.keras import activations
from keras.models import load_model
import os
import numpy as np
import tensorflow as tf
from rdflib import Graph

# Get target_accuracy from KB 
def get_target_accuracy():
    g = Graph()
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, "KB.n3")
    g.parse(file_path, format="n3")

    qres = g.query(
        """
        PREFIX ind: <URN:inds:>
        PREFIX prop: <URN:prop:>
        
        SELECT ?accuracy
        WHERE { 
            ind:Accuracy prop:hasMin ?accuracy .
        }
        """
    )

    for row in qres:
        return float(row.accuracy)  

# main function for classification
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

#get target accuracy from KB
    targetAccuracy = get_target_accuracy()

# add alarm
    if (np.max(score) < targetAccuracy):
        alarm = True
    else:
        alarm = False

# print inference result
    return ("{} ({:.2f}% probability)".format(class_names[np.argmax(score)],100 * np.max(score))), alarm
