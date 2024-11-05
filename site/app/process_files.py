import pathlib
from io import BytesIO

from pdf2image import convert_from_bytes
from sqlalchemy import exc
from PIL import Image
import numpy as np
import cv2

from optview import app
from models.files import Files
from models.files_processed import FilesProcessed
from models.files_processed_types import FilesProcessedTypes
from models.files_processed_results import FilesProcessedResults
from validate_fields import is_valid_uuid
from ml_models.table_model import TableModel
from ml_models.ocr import Ocr
import helper


SIGNATURES = {

    '.pdf': {
        'offset': 0,
        'magic_bytes_list':[
            bytes('%PDF', 'ascii'),
        ]
    },
    '.dwg': {
        'offset': 0,
        'magic_bytes_list':[
            bytes('AC1012', 'ascii'),
            bytes('AC1014', 'ascii'),
            bytes('AC1015', 'ascii'),
            bytes('AC1018', 'ascii'),
            bytes('AC1012', 'ascii'),
            bytes('AC1021', 'ascii'),
            bytes('AC1024', 'ascii'),
            bytes('AC1027', 'ascii'),
            bytes('AC1032', 'ascii'),
        ]
    },
}

def is_valid_file_type(file_data, file_name):
    suffix = pathlib.Path(file_name).suffix.lower()

    if suffix in SIGNATURES.keys():
        signature = SIGNATURES[suffix]

        for magic_bytes in signature['magic_bytes_list']:
            start = signature['offset']
            end = start + len(magic_bytes)
            if file_data[start:end] == magic_bytes:
                return True
        return False
    else:
        return False

def save_processed_file(current_user, folder_id, parent_file_id, processed_type_id, png_image, name):
    status = 'Ok'
    message = ''
    
    try:
        FilesProcessed.add(user_id=current_user.id, folder_id=folder_id, parent_file_id=parent_file_id, name=name, file=png_image, processed_type_id=processed_type_id)
    except exc.SQLAlchemyError as e:
        # TODO log error
        status = 'Error'
        message = 'Houve um erro na inserção da imagem extraida do arquivo.'

    return status, message

def save_results(plan_file_id, bank):
    status = 'Ok'
    message = ''

    try:
        for code in bank:
            item = bank[code]
            for index in range(item['count']):
                image_plan = item['images'][index]
                cv2_image_plan = np.array(image_plan)
                pil_image_plan = Image.fromarray(cv2_image_plan)
                buffer = BytesIO()
                pil_image_plan.save(buffer, format=app.config['IMAGE_TYPE'])
                bytea_image_plan = buffer.getvalue()
                
                image_plan_box = item['boxes'][index]
                image_plan_box_dict = { 'box': list(image_plan_box)}

                FilesProcessedResults.add(
                    plan_file_id=plan_file_id,
                    code=code,
                    description=None,
                    image_plan=bytea_image_plan,
                    image_plan_box=image_plan_box_dict,
                    image_table_line=None,
                    image_table_line_box=None,
                )
    except exc.SQLAlchemyError as e:
        # TODO log error
        status = 'Error'
        message = 'Houve um erro na inserção da imagem extraida do arquivo.'

    result = {
        'status': status,
        'message': message,
    }
    return result

def extract_images_from_pdf(app, current_user, file_uuid):
    status = 'Ok'
    message = ''

    file = None

    if is_valid_uuid(file_uuid):
        file = Files.get_one(user_id=current_user.id, uuid=file_uuid)

    if not is_valid_uuid(file_uuid):
        status = 'Error'
        message = f"A UUID do arquivo é inválida."
    elif file is None:
        status = 'Error'
        message = f"O arquivo com UUID '{file_uuid}' não existe."
    else:
        name_stem = pathlib.Path(file.name).stem
        file_processed_type = app.config['PROCESSED_FILE_TYPE_EXTRACTED_IMAGE']
        processed_type_id = FilesProcessedTypes.get_one(file_processed_type=file_processed_type).id
        files_processed = FilesProcessed.get_all(user_id=current_user.id, parent_file_id=file.id, processed_type_id=processed_type_id)
        if len(files_processed) == 0:
            # image not extracted: extract
            images = convert_from_bytes(file.file, fmt=app.config['EXTRACTED_IMAGE_TYPE'])

            page_count = len(images)
            for index in range(page_count):
                pil_image = images[index]
                buffer = BytesIO()
                pil_image.save(buffer, format=app.config['IMAGE_TYPE'])
                image = buffer.getvalue()

                # change file name and number it
                name_index = ''
                if index != 0:
                    name_index = '_' + str(index)

                name = f'{name_stem}{name_index}.{app.config["IMAGE_TYPE"].lower()}'

                status, message = save_processed_file(current_user, file.folder_id, file.id, processed_type_id, image, name)

    return status, message

def extract_tables_from_image(app, current_user, file_uuid):
    status = 'Ok'
    message = ''

    file = None

    if is_valid_uuid(file_uuid):
        file = Files.get_one(user_id=current_user.id, uuid=file_uuid)

    if not is_valid_uuid(file_uuid):
        status = 'Error'
        message = f"A UUID do arquivo é inválida."
    elif file is None:
        status = 'Error'
        message = f"O arquivo com UUID '{file_uuid}' não existe."
    else:
        file_processed_type = app.config['PROCESSED_FILE_TYPE_EXTRACTED_IMAGE']
        processed_type_id = FilesProcessedTypes.get_one(file_processed_type=file_processed_type).id
        files_already_processed = FilesProcessed.query.filter(
            FilesProcessed.user_id == current_user.id, 
            FilesProcessed.parent_file_id == file.id,
            FilesProcessed.processed_type_id != processed_type_id,
        ).all()
        if len(files_already_processed) == 0:
            # no files processed: process
            extracted_image_type = app.config['PROCESSED_FILE_TYPE_EXTRACTED_IMAGE']
            extracted_image_type_id = FilesProcessedTypes.get_one(file_processed_type=extracted_image_type).id
            legend_type = app.config['PROCESSED_FILE_TYPE_LEGEND']
            legend_type_id = FilesProcessedTypes.get_one(file_processed_type=legend_type).id
            plan_type = app.config['PROCESSED_FILE_TYPE_PLAN']
            plan_type_id = FilesProcessedTypes.get_one(file_processed_type=plan_type).id

            model = TableModel(app)

            for file_processed in file.files_processed:
                # process only extracted images
                if file_processed.processed_type_id == extracted_image_type_id:
                    tables_images_data = model.extract_tables(file_processed.name, file_processed.file)
                    plan_image_data = file_processed.file
                    plan_image = Image.open(BytesIO(plan_image_data))

                    for image_data in tables_images_data:
                        name = image_data['name']
                        png_image = image_data['image_data']
                        status, message = save_processed_file(current_user, file.folder_id, file.id, legend_type_id, png_image, name)
                        if status != 'Ok': 
                            break

                        # clear each table on the original image
                        box_bounds = image_data['box_bounds']
                        white_color = (255, 255, 255)
                        plan_image.paste(white_color, box_bounds)
                       
                        if status != 'Ok': 
                            break

                    if status == 'Ok':
                        png_plan_image = model.pil_image_to_bytes(plan_image)
                        plan_file_name = model.get_new_file_name(file.name, 'plan')
                        status, message = save_processed_file(current_user, file.folder_id, file.id, plan_type_id, png_plan_image, plan_file_name)

    return status, message

def divide_image_with_overlap(image, num_rows=6, num_cols=6, overlap=20, sub_width=0, sub_height=0):
    sub_images = []
    coordinates = []
    height, width = image.shape[:2]

    if sub_width > 0 and sub_height > 0:
        num_cols = width // sub_width + (1 if width % sub_width != 0 else 0)
        num_cols = height // sub_height + (1 if height % sub_height != 0 else 0)
    else:
        sub_width = width // num_cols
        sub_height = height // num_rows

    for row in range(num_rows):
        for col in range(num_cols):
            start_row = max(row * sub_height - overlap, 0)
            end_row = min(start_row + sub_height + 2 * overlap, height)
            start_col = max(col * sub_width - overlap, 0)
            end_col = min(start_col + sub_width + 2 * overlap, width)

            sub_image = image[start_row:end_row, start_col:end_col]
            sub_images.append(sub_image)
            coordinates.append((start_row, start_col))

    return sub_images, coordinates

def get_first_column(img_table):
    # img_table must be a opencv image in grayscale

    # uses the 3/4 bottom part to avoid headers
    width = img_table.shape[1]
    height = 3 * img_table.shape[0] // 4
    img_threshold0 = img_table[-height:,:]

    # remove gray backgrounds
    _, img_threshold0 = cv2.threshold(img_threshold0, 100, 255, cv2.THRESH_BINARY)

    # remove vertical lines
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
    img_threshold0 = cv2.dilate(img_threshold0, vertical_structure)

    # blur deeply
    img_blured = img_threshold0
    for i in range(1,10):
        img_blured = cv2.blur(img_blured, (5, 1))

    # keeps only black areas
    _, img_threshold = cv2.threshold(img_blured, 254, 255, cv2.THRESH_BINARY)

    # remove horizontal lines
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))
    img_dilated = cv2.dilate(img_threshold, horizontal_structure)
    _, img_threshold2 = cv2.threshold(img_dilated, 254, 255, cv2.THRESH_BINARY)

    # find the first colum position
    min_columns = np.min(img_threshold2, axis=0)
    first_zero_column = min_columns.argmin()
    min_columns_cropped = min_columns[first_zero_column:]
    second_zero_colum = min_columns_cropped.argmax()
    x = first_zero_column + second_zero_colum

    # crop the original image to get only the first column
    return img_table[:,0:x]

def legends_pre_processing(app, files_processed):
    legend_type = app.config['PROCESSED_FILE_TYPE_LEGEND']
    legend_type_id = FilesProcessedTypes.get_one(file_processed_type=legend_type).id

    images_first_columns = []
    for file_processed in files_processed:
        if file_processed.processed_type_id == legend_type_id:
            png_image = file_processed.file
            pil_image = Image.open(BytesIO(png_image))
            # IMPORTANT: must be in grayscale opencv image
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
            
            img_first_column = get_first_column(opencv_image)
            images_first_columns.append(img_first_column)
   
    return images_first_columns

def legend_processing(ocr_results):
    def is_number(s):
        try:
            int(s)
            float(s)
            return True
        except ValueError:
            return False

    target_words = []
    final_targets = []
    for legend in ocr_results:
        contagem_componentes = {}
        for word in legend[0]:
            if len(word[0]) >= 3 and is_number(word[0]) == False:
                target_words.append(word[0])
                # Use word[0] (presumably the word string) as the key instead of the entire word array
                if word[0] in contagem_componentes:
                    contagem_componentes[word[0]] += 1
                else:
                    contagem_componentes[word[0]] = 1
          
    for item, count in contagem_componentes.items():
        # Correctly iterate through dictionary items
        if count > 1:
            # Use count instead of iten.value()
            for i in range(1, count + 1):
                if count >= 10:
                    final_targets.append(item + str(i))
                else:
                    final_targets.append(item + '0' + str(i))
        else:
            final_targets.append(item)

    return target_words, final_targets

def locate_targets(image ,target_words, adjusted_word_info, overlap=25):
    encontrados = []
    for item in adjusted_word_info:
        if item[0].lower() in target_words:
            encontrados.append(item)

    target_crops = []
    bound_boxes = []
    for word in encontrados:
        pontos = word[1]
        x_inicial = min(pontos[0][0], pontos[1][0], pontos[2][0], pontos[3][0])  # - overlap
        y_inicial = min(pontos[0][1], pontos[1][1], pontos[2][1], pontos[3][1])  # - overlap
        x_final = max(pontos[0][0], pontos[1][0], pontos[2][0], pontos[3][0]) + overlap
        y_final = max(pontos[0][1], pontos[1][1], pontos[2][1], pontos[3][1]) + overlap

        x_inicial, y_inicial, x_final, y_final = map(int, [x_inicial, y_inicial, x_final, y_final])
        target_crops.append(image[y_inicial:y_final, x_inicial:x_final])
        bound_boxes.append((x_inicial, y_inicial, x_final, y_final))

    return target_crops, bound_boxes

def process_images(app, files_processed):
    result = {
        'status': 'Ok',
        'message': ''
    }

    ocr = Ocr(app)

    images_first_columns = legends_pre_processing(app, files_processed)

    plan_type = app.config['PROCESSED_FILE_TYPE_PLAN']
    plan_type_id = FilesProcessedTypes.get_one(file_processed_type=plan_type).id

    for file_processed in files_processed:
        if file_processed.processed_type_id == plan_type_id:
            png_image = file_processed.file
            pil_image = Image.open(BytesIO(png_image))
            numpy_image = np.asarray(pil_image)

            sub_images, coordinates = divide_image_with_overlap(numpy_image)
            adjusted_word_info = ocr.apply_ocr(sub_images, coordinates)
            ocr_results = ocr.legend_ocr(images_first_columns)
            target, final = legend_processing(ocr_results)
            target_crops, target_boxes = locate_targets(numpy_image, target, adjusted_word_info)
            bank = ocr.count_targets(target, final, target_crops, target_boxes)

            result = save_results(file_processed.id, bank)
            if result['status'] != 'Ok':
                break

    return result
