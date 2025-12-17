import datetime
from utils import get_route_function_name, send_response, get_post_data, get_cookies, on_not_login_redirect, has_error
import database
import html

# Routes handle
def handle_request(method, request):
    try:
        # Get route funtion name
        route_function_name = get_route_function_name(method, request.path)
        
        # If the route function exists in the script, run the function
        if route_function_name in globals():
            # Get the router function
            route_function = globals()[route_function_name]
            # Call the router funtion passing the request
            route_function(request)
        # If the route doesn't exists, return "not found"
        else:
            status = 404
            headers = []
            content = "Page not found"
            send_response(request, status, headers, content)
    except Exception as error:
        print(error)

        status = 500
        headers = []
        content = "Internal server error"
        send_response(request, status, headers, content)

# Routes

# GET /
def get_index(request):
    on_not_login_redirect(request)
    
    cookies = get_cookies(request)

    template_content = open('templates/index.html').read()

    user_info = f"{cookies['user_name']} ({cookies['user_role']})"

    template_content = template_content.replace('<span id="user-info"></span>', user_info)

    messages = database.get_messages()

    messages_html = '<div>'
    for message in messages:
        # Decrypt protected information
        phone_decrypted = database.fernet.decrypt(message[6].encode()).decode()

        # Escape data
        title_safe = html.escape(message[1] or '')
        text_safe = html.escape(message[2] or '')
        author_safe = html.escape(message[5] or '')
        phone_safe = html.escape(phone_decrypted or '')
        date_safe = html.escape(message[3] or '')

        messages_html += f"""
            <div>
                <h2>{title_safe}</h2>
                
                <p>{text_safe}</p>

                <i>By {author_safe} ({phone_safe}) at {date_safe}</i>
            </div>

            <hr />
        """
    messages_html += '</div>'

    template_content = template_content.replace('<div id="messages"></div>', messages_html)

    status = 200
    headers = []
    content = template_content
    send_response(request, status, headers, content)
 
# GET /login
def get_login(request):    
    template_content = open('templates/login.html').read()

    if has_error(request):
        error_info = "<p>Incorrect Username or Password</p>"
        template_content = template_content.replace('<span id="error-info"></span>', error_info)

    status = 200
    headers = []
    content = template_content
    send_response(request, status, headers, content)

# POST /login
def post_login(request):
    data = get_post_data(request)

    user = database.login(data['username'], data['password'])

    if user:
        status = 303
        headers = [
            {'name': 'Location', 'value': '/'},
            {'name': 'Set-Cookie', 'value': f"user_id={user[0]}"},
            {'name': 'Set-Cookie', 'value': f"user_name={user[1]}"},
            {'name': 'Set-Cookie', 'value': f"user_role={user[5]}"},
        ]
        content = ""
        send_response(request, status, headers, content)
    else:
        # Write failed loging into the log file
        with open('noticeboard.auth.log', "a") as f:
            ip = request.client_address[0]
            user = data['username']
            date = datetime.datetime.now()
            f.write(f"FAILED_LOGIN ip={ip} user={user} date={date}\r\n")

        status = 303
        headers = [
            {'name': 'Location', 'value': '/login?error=True'},
        ]
        content = ""
        send_response(request, status, headers, content)

# GET /logout
def get_logout(request):
    status = 303
    headers = [
        {'name': 'Location', 'value': '/login'},
        {'name': 'Set-Cookie', 'value': "user_id="},
        {'name': 'Set-Cookie', 'value': "user_name="},
        {'name': 'Set-Cookie', 'value': "user_role="},
    ]
    content = ""
    send_response(request, status, headers, content)

# GET /register
def get_register(request):
    template_content = open('templates/register.html').read()

    if has_error(request):
        error_info = "<p>The user could not be added</p>"
        template_content = template_content.replace('<span id="error-info"></span>', error_info)

    status = 200
    headers = []
    content = template_content
    send_response(request, status, headers, content)

# POST /register
def post_register(request):
    data = get_post_data(request)

    id = database.add_user(data['name'], data['phone'], data['username'], data['password'])

    if id:
        status = 303
        headers = [
            {'name': 'Location', 'value': '/login'}
        ]
        content = ""
        send_response(request, status, headers, content)
    else:
        status = 303
        headers = [
            {'name': 'Location', 'value': '/register'}
        ]
        content = ""
        send_response(request, status, headers, content)
   
# GET /addmessage
def get_addmessage(request):
    on_not_login_redirect(request)

    cookies = get_cookies(request)

    template_content = open('templates/addmessage.html').read()
    
    if has_error(request):
        error_info = "<p>The message could not be added</p>"
        template_content = template_content.replace('<span id="error-info"></span>', error_info)

    user_info = f"{cookies['user_name']} ({cookies['user_role']})"

    template_content = template_content.replace('<span id="user-info"></span>', user_info)

    status = 200
    headers = []
    content = template_content
    send_response(request, status, headers, content)

# POST /addmessage
def post_addmessage(request):
    cookies = get_cookies(request)
    data = get_post_data(request)

    message_id = database.add_message(data['title'], data['message'], cookies['user_id'])

    if message_id:
        status = 303
        headers = [
            {'name': 'Location', 'value': '/'},
        ]
        content = ""
        send_response(request, status, headers, content)
    else:
        status = 303
        headers = [
            {'name': 'Location', 'value': '/addmessage?error=True'}
        ]
        content = ""
        send_response(request, status, headers, content)
