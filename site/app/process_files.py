import pathlib
import io

import pypdfium2 as pdfium 
from sqlalchemy import exc

from models.files import Files
from models.files_processed import FilesProcessed
from models.files_processed_types import FilesProcessedTypes
from validate_fields import is_valid_uuid


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
                buffer = io.BytesIO()
                pil_image.save(buffer, format='PNG')
                png_image = buffer.getvalue()

                # change file name and number it
                name_index = ''
                if index != 0:
                    name_index = '_' + str(index)

                name = f'{name_stem}{name_index}.png'

                try:
                    FilesProcessed.add(user_id=current_user.id, parent_file_id=file.id, name=name, file=png_image, processed_type_id=processed_type_id)
                except exc.SQLAlchemyError as e:
                    # TODO log error
                    status = 'Error'
                    message = 'Houve um erro na inserção da imagem extraida do arquivo.'

    return status, message
