import pathlib
from io import BytesIO

import pypdfium2 as pdfium
from sqlalchemy import exc
from PIL import Image

from models.files import Files
from models.files_processed import FilesProcessed
from models.files_processed_types import FilesProcessedTypes
from validate_fields import is_valid_uuid
from ml_models.table_model import TableModel


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

def extract_images_from_pdf(app, current_user, file_uuid):
    status = 'Ok'
    message = ''

    file = None

    if is_valid_uuid(file_uuid):
        file = Files.get_one(user_id = current_user.id, uuid = file_uuid)

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
            pdf = pdfium.PdfDocument(file.file)

            page_count = len(pdf)
            for index in range(page_count):
                page = pdf[index]
                bitmap = page.render(scale=200/72)
                pil_image = bitmap.to_pil()
                buffer = BytesIO()
                pil_image.save(buffer, format='PNG')
                png_image = buffer.getvalue()

                # change file name and number it
                name_index = ''
                if index != 0:
                    name_index = '_' + str(index)

                name = f'{name_stem}{name_index}.png'

                status, message = save_processed_file(current_user, file.folder_id, file.id, processed_type_id, png_image, name)

    return status, message

def extract_tables_from_image(app, current_user, file_uuid):
    status = 'Ok'
    message = ''

    file = None

    if is_valid_uuid(file_uuid):
        file = Files.get_one(user_id = current_user.id, uuid = file_uuid)

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