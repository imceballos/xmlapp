import base64

def decode_from_base64(folder: str):

    encoded_bytes = folder.encode('ascii')
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_text = decoded_bytes.decode('ascii')
    return decoded_text


def encode_to_base64(folder: str):

    encoded_bytes = folder.encode('ascii')
    decoded_bytes = base64.b64encode(encoded_bytes)
    decoded_text = decoded_bytes.decode('ascii')
    return decoded_text

def decode_from_base_alternative(file):
    return base64.b64decode(file)

def encode_to_base64_alternative(file):
    file_input=open(file, "rb")
    file_encoded=base64.b64encode(file_input.read())
    return file_encoded
