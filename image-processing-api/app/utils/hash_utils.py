import base64

def compress_url(url: str) -> str:
    # Encode the URL to bytes, then to Base64, and finally decode to a string
    compressed = base64.urlsafe_b64encode(url.encode()).decode()

    # Replace non-filename-friendly characters
    compressed = compressed.replace('=', '').replace('/', '_')

    return compressed

def decompress_url(compressed: str) -> str:
    # Replace the characters back to their original Base64 form
    compressed = compressed.replace('_', '/')

    # Decode from Base64 to bytes, then to string
    url = base64.urlsafe_b64decode(compressed + '==').decode()

    return url
