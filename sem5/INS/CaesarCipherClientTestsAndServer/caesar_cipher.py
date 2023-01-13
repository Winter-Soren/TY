_ASCII_RANGE = 128

def GenerateCaesarCipher(message, shift):
    """Generates a caesar cipher for a given message based on the given shift.
    Only supports ASCII. Shifts that go out of bounds of 0-127 wrap around.

    Args:
        message (string) - Message to perform the caesar cipher on.
        shift (int) - Amount each letter is shifted to get the ciphered letter.

    Returns:
        (string) The ciphered message.
    """

    if type(message) is not str:
        raise ValueError('Message must be a string!')
    elif type(shift) is not int:
        raise ValueError('Shift must be an integer!')
    ret = ""

    for i in message:
        future_value = (ord(i) + shift) % _ASCII_RANGE
        ret += chr(future_value)

    return ret
