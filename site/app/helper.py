import numpy as np
import cv2
import pickle

def save(name, images):
    path = '/home/agranero/Dropbox/Code/Python/optiview_tech1/tests/'
    if isinstance(images, list):
        for index, image in enumerate(images):
            if isinstance(images, np.ndarray):
                cv2.imwrite(f'{path}{name}_{index}.png', image)
            else:
                cv2.imwrite(f'{path}{name}_{index}.png', np.array(image))

    else:
        if isinstance(images, np.ndarray):
            cv2.imwrite(f'{path}{name}.png', image)
        else:
            cv2.imwrite(f'{path}{name}.png', np.array(images))

def save_object(name, object):
    path = '/home/agranero/Dropbox/Code/Python/optiview_tech1/tests/'
    file_name = f'{path}{name}.pkl'
    with open(file_name, 'wb') as file:
        pickle.dump(object, file)

def load_object(name):
    path = '/home/agranero/Dropbox/Code/Python/optiview_tech1/tests/'
    file_name = f'{path}{name}.pkl'
    with open(file_name, 'rb') as file:
        object = pickle.load(file)

    return object