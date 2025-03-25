from PIL import Image
import base64

def text_to_binary(text: str) -> str:
    """Convert text to binary."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary: str) -> str:
    """Convert binary to text."""
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def encode_text_in_image(image_path: str, text: str, output_path: str):
    """Embed text inside an image using LSB steganography."""
    img = Image.open(image_path)
    binary_text = text_to_binary(text) + '1111111111111110'  # End of message marker

    pixels = list(img.getdata())
    new_pixels = []

    binary_index = 0
    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # Modify R, G, B
            if binary_index < len(binary_text):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_text[binary_index])
                binary_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_path)

def decode_text_from_image(image_path: str) -> str:
    """Extract hidden text from an image."""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_text = ""
    for pixel in pixels:
        for i in range(3):  # Read R, G, B
            binary_text += str(pixel[i] & 1)

    # Extract the message until the end marker
    message_end = binary_text.find('1111111111111110')
    if message_end != -1:
        binary_text = binary_text[:message_end]

    return binary_to_text(binary_text)
