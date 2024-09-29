def encrypt_message(message, shift=3):
    """Encrypt a message using a simple Caesar cipher."""
    encrypted = ""
    for char in message:
        if char.isalpha():
            shift_char = ord(char) + shift
            if char.islower():
                if shift_char > ord('z'):
                    shift_char -= 26
            elif char.isupper():
                if shift_char > ord('Z'):
                    shift_char -= 26
            encrypted += chr(shift_char)
        else:
            encrypted += char
    return encrypted

def decrypt_message(encrypted_message, shift=3):
    """Decrypt a message using a simple Caesar cipher."""
    return encrypt_message(encrypted_message, -shift)
