import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("defect_classifier.h5")

img = image.load_img("test10.png", target_size=(224,224))
x = image.img_to_array(img) / 255.0
x = np.expand_dims(x, axis=0)

pred = model.predict(x)[0][0]

print("Confidence:", pred)

if pred < 0.5:
    print("DEFECTIVE")
else:
    print("NON-DEFECTIVE")
