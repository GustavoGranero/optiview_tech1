import os
from pathlib import Path
from io import BytesIO

from ultralytics import YOLO
from PIL import Image

class TableModel:
    model = None

    def __init__(self, app):
        self.app = app

        # initialize class attribute just the first time
        # TODO better store it on optviview.py and import it like db
        if TableModel.model is None:
            TableModel.model = YOLO(self.get_weights_filename())
            TableModel.model.to('cpu')

    def get_weights_filename(self):
        filename = os.path.join(os.path.dirname(__file__), self.app.config['TABLE_WEIGHTS'])  
        return filename
    
    def get_new_file_name(self, original_name, file_type, index=0):
        name_stem = Path(original_name).stem
        # change file name and number it
        name_index = ''
        if index != 0:
            name_index = '_' + str(index)

        new_name = f'{name_stem}_{file_type}{name_index}.png'
        return new_name
    
    def pil_image_to_bytes(self, pil_image):
            buffer = BytesIO()
            pil_image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            return image_bytes

    def extract_tables(self, file_name, file_data):
        image = Image.open(BytesIO(file_data))

        images_data = []
        results = self.model.predict(image, imgsz=3008, conf=0.5, device='cpu')
        result = results[0]
        for index, box in enumerate(result.boxes):
            if self.model.names[int(box.cls)] == 'table':
                # only uses table class
                # crop image to get the table found
                box_bounds = tuple(map(int, box.xyxy[0]))
                table_image = image.crop(box_bounds)
                image_data = self.pil_image_to_bytes(table_image)
                new_name = self.get_new_file_name(file_name, 'legend', index)
                image_data = {
                    'name': new_name,
                    'image_data': image_data,
                    'box_bounds': box_bounds
                }
                images_data.append(image_data)

        return images_data
