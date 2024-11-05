import keras_ocr
import cv2
import numpy as np

class Ocr:
    pipeline = None

    def __init__(self, app):
        self.app = app

        # initialize class attribute just the first time 
        # TODO better store it on optviview.py and import it like db
        if Ocr.pipeline is None:
            Ocr.pipeline = keras_ocr.pipeline.Pipeline()

    def apply_ocr(self, sub_images, coordinates):
        sub_images_ocr = []
        adjusted_word_info = []

        for sub_img in sub_images:
            prediction_groups = Ocr.pipeline.recognize([sub_img])
            # prediction_groups is list of (word, box) tuples.
            sub_images_ocr.append(prediction_groups[0])

        for word_info, (offset_y, offset_x) in zip(sub_images_ocr, coordinates):
            adjusted_words = []
            for word, box in word_info:
                adjusted_box = box + [offset_x, offset_y]
                adjusted_words.append((word, adjusted_box))

            adjusted_word_info.extend(adjusted_words)

        return adjusted_word_info
    
    def legend_ocr(self, fist_column_images):
        prediction_groups = []
        for first_column_image in fist_column_images:
            prediction_groups.append(Ocr.pipeline.recognize([cv2.cvtColor(first_column_image, cv2.COLOR_GRAY2RGB)]))

        return prediction_groups
    
    def count_targets(self, target_words, final_targets, target_crops, target_boxes):
        crops_ocr = []
        for crop in target_crops:
            prediction_groups = Ocr.pipeline.recognize([crop])
            # prediction_groups is list of (word, box) tuples.
            crops_ocr.append(prediction_groups[0])

        codigos = []
        imagens = []
        boxes = []
        for index, ocr in enumerate(crops_ocr):
            alvo = ''
            outros = []
            for item in ocr:
                if item[0].lower() in target_words:
                    alvo = item[0].lower()
                else:
                    outros.append(item[0].lower())

            for item in outros:
                word = alvo + item
                if word in final_targets:
                    codigos.append(word)
                    imagens.append(target_crops[index])
                    boxes.append(target_boxes[index])
        
        bank = {}
        for index, codigo in enumerate(codigos):
            if codigo in bank:
                bank[codigo]['count'] += 1
                bank[codigo]['images'].append(imagens[index])
                bank[codigo]['boxes'].append(boxes[index])
            else:
                elemento = {
                    'count': 1,
                    'images': [imagens[index]],
                    'boxes': [boxes[index]]
                }
                bank[codigo] = elemento

        return bank
