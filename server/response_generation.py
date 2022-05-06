from re import X
from tkinter import Y


def get_status_message_from_code(status_code: int):
    if status_code == 200:
        return 'OK'
    elif status_code == 404:
        return 'Not Found'
    
    else:
        return 'Undefined'

def generate_response_message(protocol: str, status_code: int, extra_headers_lines: str, body: str, status_only: bool):
    status_message = get_status_message_from_code(status_code)
    

    status_line = f"{protocol} {status_code} {status_message}\r\n"

    if status_only:
        return status_line


    lines = [status_line, *extra_headers_lines, body,  "\r\n"]

    response_message = ""
    for line in lines:
        response_message += line

    return response_message


def get_response_by_verb(protocol:str, verb: str, success: bool, body: str):

    status_code = 200 if success else 404

    if verb == 'GET':
        return generate_response_message(protocol, status_code, [], body, False)
    elif verb == 'POST':
        return generate_response_message(protocol, status_code, [], '', True)


x = get_response_by_verb('HTTP/1.1', 'GET', True, 'THIS IS THE BODY')
print(x)