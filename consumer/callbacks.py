def user_info_callback(ch, method, properties, body):
    del ch, method, properties
    print('Callback: user_info_callback')
    print(body.decode('UTF-8'))

def user_error_callback(ch, method, properties, body):
    del ch, method, properties
    print('Callback: user_error_callback')
    print(body.decode('UTF-8'))

def oder_info_callback(ch, method, properties, body):
    del ch, method, properties
    print('Callback: oder_info_callback')
    print(body.decode('UTF-8'))

def oder_error_callback(ch, method, properties, body):
    del ch, method, properties
    print('Callback: oder_error_callback')
    print(body.decode('UTF-8'))
