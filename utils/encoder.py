import numpy as np
from PIL import Image
from utils.constants import DELIMITER

def text_to_binary(text):
    """
    Converts a string of text into a sequence of binary digits (0s and 1s).
    """
    binary_str = ""
    for char in text:
        binary_char = format(ord(char), '08b')
        binary_str += binary_char
    return binary_str

def encode(image_path, secret_message, output_path):
    """
    Embeds a secret message into an image using LSB (Least Significant Bit) steganography.
    """
    message_with_delimiter = secret_message + DELIMITER
    binary_message = text_to_binary(message_with_delimiter)
    message_len = len(binary_message)

    img = Image.open(image_path)
    img = img.convert('RGB')
    
    pixel_data = np.array(img)
    flat_data = pixel_data.flatten()
    
    if message_len > len(flat_data):
        raise ValueError(f"Message is too long. Capacity: {len(flat_data)} bits. Message: {message_len} bits.")
    
    for i in range(message_len):
        flat_data[i] = (flat_data[i] & 254) | int(binary_message[i])
    
    stego_data = flat_data.reshape(pixel_data.shape)
    stego_img = Image.fromarray(stego_data.astype('uint8'), 'RGB')
    stego_img.save(output_path)
    print(f"[+] Successfully encoded message into {output_path}")
