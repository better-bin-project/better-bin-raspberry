import tensorflow as tf
import numpy as np
import stepper
import argparse
import os
import RPi.GPIO as GPIO

TOTAL_STEPS = 14000
STEPS_BOX = 3100
STEPS_DELAY = 0.0005
BUTTON_PIN = 17

STEPS_PAPER = 0
STEPS_RESIDUAL = int(TOTAL_STEPS / 2)
STEPS_PLASTIC = TOTAL_STEPS

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', default='resnet50',
    choices=['resnet50', 'vgg16', 'mobilenet'])
args = vars(parser.parse_args())

models_dict = {
    'resnet50': tf.keras.applications.resnet50.ResNet50(weights='imagenet'),
    'vgg16': tf.keras.applications.vgg16.VGG16(weights='imagenet'),
    'mobilenet': tf.keras.applications.mobilenet_v2.MobileNetV2(weights='imagenet'),
}

img_dict = {
    'paper_towel': 'paper',
    'toilet_tissue': 'paper',
    'bath_towel': 'paper',
    'gown': 'paper',
    'carton': 'paper',
    'envelope': 'paper',
    'packet': 'paper',
    'menu': 'paper',
    'medicine_chest': 'paper',
    'handkerchief': 'paper',
    'hard_disk': 'paper',
    'wool': 'paper',
    'conch': 'paper',
    'diaper': 'paper',
    'mixing_bowl': 'paper',
    'cup': 'paper',
    'coffee_mug': 'paper',

    'plastic_bag': 'plastic',
    'shower_cap': 'plastic',
    'mosquito_net': 'plastic',
    'bassinet': 'plastic',
    'measuring_cup': 'plastic',
    'beaker': 'plastic',
    'sleeping_bag': 'plastic',
    'beer_glass': 'plastic',
    'pop_bottle': 'plastic',
    'shower_curtain': 'plastic',
    'cocktail_shaker': 'plastic',
    'water_bottle': 'plastic',
    'water_jug': 'plastic',
    'combination_lock': 'plastic',
    'safe': 'plastic',
    'binder': 'plastic',
    'window_screen': 'plastic',
    'great_white_shark': 'plastic',
    'wine_bottle': 'plastic',
    'bubble': 'plastic',
    'washer': 'plastic'
}

def recognize(modelname, imgpath):
    image = tf.keras.preprocessing.image.load_img(imgpath,
        target_size=(224, 224))
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.imagenet_utils.preprocess_input(image)
    model = models_dict[modelname]
    predictions = model.predict(image)
    processed_preds = tf.keras.applications.imagenet_utils.decode_predictions(
        preds=predictions
    )

    print(f"Processed predictions: {processed_preds}")
    print('-' * 50)

    print("Prediction: ")
    print(f"  {imgpath}: {processed_preds[0][0][1]} to {processed_preds[0][0][2]}")
    return (processed_preds[0][0][1], processed_preds[0][0][2])

currentPos = 0
currentButtonPos = bool(GPIO.input(BUTTON_PIN))

try:
    stepper.doSteps(1, -TOTAL_STEPS, STEPS_DELAY)

    print("Ready. Enter 'next' to classify a piece of trash.")
    while True:
        if (bool(GPIO.input(BUTTON_PIN)) != currentButtonPos) or input() == "next":
            currentButtonPos = not currentButtonPos

            os.system("libcamera-still -o img.jpg")
            res, prob = recognize(args['model'], 'img.jpg')
            print(res, prob)
            category = 'residual'
            if res in img_dict:
                category = img_dict[res]

            if (category == 'paper'):
                stepper.doSteps(1, STEPS_PAPER - currentPos, STEPS_DELAY)
                currentPos = STEPS_PAPER
            elif (category == 'plastic'):
                stepper.doSteps(1, STEPS_PLASTIC - currentPos, STEPS_DELAY)
                currentPos = STEPS_PLASTIC
            else:
                stepper.doSteps(1, STEPS_RESIDUAL - currentPos, STEPS_DELAY)
                currentPos = STEPS_RESIDUAL

            stepper.doSteps(2, STEPS_BOX, STEPS_DELAY)
            stepper.doSteps(2, -STEPS_BOX, STEPS_DELAY)
            print("Ready. Enter 'next' to classify a piece of trash.")

except KeyboardInterrupt():
    pass