import re


def clean_txt(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)

    # Remove URLs
    text = re.sub(r'https?://[a-zA-Z0-9$-_@.&+!*(),%]+', '', text)

    # Remove special characters, keep alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)

    # Trim leading and trailing whitespace
    text = text.strip()

    return text

# Newline at the end of the file to adhere to PEP 8
