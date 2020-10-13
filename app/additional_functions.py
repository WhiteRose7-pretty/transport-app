from cryptography.fernet import Fernet

#funkcja kodowania
def code_function(input):
    key = 'LZrGOSiFE7bMmDLuQPQSd6KD-eBqBOWNfgLUVI3rMqw=' #SECRET KEY
    input_on_b = bytes('%s' % (input), encoding='UTF-8')
    cipher_suite = Fernet(key)
    coded_text = cipher_suite.encrypt(input_on_b)
    return str(coded_text, encoding='UTF-8')


#funkcja dekofowania
def decode_function(input):
    key = 'LZrGOSiFE7bMmDLuQPQSd6KD-eBqBOWNfgLUVI3rMqw=' #SECRET KEY
    input_on_b = bytes('%s' % (input), encoding='UTF-8')
    cipher_suite = Fernet(key)
    decoded_text = cipher_suite.decrypt(input_on_b)
    return decoded_text.decode('utf-8')