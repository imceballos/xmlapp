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