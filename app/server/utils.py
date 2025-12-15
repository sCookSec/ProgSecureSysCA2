def get_route_function_name(method, path):
    # Get router path
    router_path_name = path[1:].split('?')[0].replace('/', '_')
    
    if router_path_name == '':
        router_path_name = 'index'
    
    # Build route funtion name
    route_function_name = f"{method}_{router_path_name}"
    
    return route_function_name

# Send response
def send_response(request, status, headers, content):
    request.send_response(status)
    for header in headers:
        request.send_header(header["name"], header["value"])
    request.end_headers()
    request.wfile.write(bytes(content, 'utf-8'))

# GET Cookies
def get_cookies(request):
    cookies = request.headers['Cookie']
    cookies_parsed = {}

    if cookies:
        for cookie in cookies.split(';'):
            key = cookie.split('=')[0].strip()
            value = cookie.split('=')[1].strip()

            cookies_parsed[key] = value

    return cookies_parsed

# Get POST data
def get_post_data(request):
    content_length = int(request.headers['Content-Length'])
    post_data = request.rfile.read(content_length).decode('utf-8')

    data_parsed = {}
    
    for data in post_data.split('\r\n'):
        if data != '':
            key = data.split('=')[0]
            value = data.split('=')[1]
            
            data_parsed[key] = value

    return data_parsed

# If not login, redirect
def on_not_login_redirect(request):
    cookies = get_cookies(request)

    if not cookies.get('user_id'):
        status = 303
        headers = [
            {'name': 'Location', 'value': '/login'}
        ]
        content = ""
        send_response(request, status, headers, content)

# Check if the redirect has and error to notify
def has_error(request):
    if len(request.path.split("?error=")) > 1:
        return True
    else:
        return False