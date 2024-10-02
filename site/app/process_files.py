import pathlib

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
