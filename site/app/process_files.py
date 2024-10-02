import pathlib
import io

import pypdfium2 as pdfium 

from models.files import Files
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

def get_images_from_pdf(current_user, file_uuid):
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
        pdf = pdfium.PdfDocument(file)

        page_count = len(pdf)
        for index in range(page_count):
            page = pdf[index]
            pil_image = page.render(scale=200/72).to_pil()
            png_image = io.BytesIO()
            pil_image.save(png_image, format='PNG')
            
            # TODO insert png_image on database
            pass

    status = {
        'status': status,
        'message': message,
    }
    return status


    

