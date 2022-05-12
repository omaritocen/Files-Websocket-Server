FORMAT = 'utf-8'
 
 
def get_status_message_from_code(status_code: int):
    if status_code == 200:
        return 'OK'
    elif status_code == 404:
        return 'Not Found'
 
    else:
        return 'Undefined'
 
 
def generate_response_message(protocol: str, status_code: int, extra_headers_lines: str, status_only: bool, body=None):
    status_message = get_status_message_from_code(status_code)
 
    status_line = f"{protocol} {status_code} {status_message}\r\n"
    print(status_line)
    if status_only:
        return status_line
 
    # Check if we need extra \r\n
    lines = [status_line, *extra_headers_lines, "\r\n"]
 
    # if body is not None:
    #     lines.insert(len(lines) - 1, body)
    # lines.insert(len(lines) - 1, "\r\n")
 
    response_message = ""
    for line in lines:
        response_message += line
 
    encoded_message = response_message.encode(FORMAT)
 
    if body is not None:
        return encoded_message + body + b"\r\n"
    else:
        return encoded_message + b"\r\n"
 
 
def get_response_by_verb(protocol: str, verb: str, success: bool, body: bytes = None):
    status_code = 200 if success else 404
 
    if verb == 'GET':
        return generate_response_message(protocol, status_code, [], False, body)
    elif verb == 'POST':
        return generate_response_message(protocol, status_code, [], True)
 