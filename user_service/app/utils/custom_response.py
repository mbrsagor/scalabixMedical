def prepare_login_response(token, role, email, full_name):
    return {
        "status": True,
        "message": "Login successful",
        "token": token,
        "role": role,
        "email": email,
        "full_name": full_name,
    }


def prepare_register_response(user):
    return {
        "status": True,
        "message": "User registered successfully",
        "data": user,
    }

def prepare_error_response(message, status_code=400):
    return {
        "status": False,
        "message": message,
        "status_code": status_code,
    }


def prepare_success_response(data):
    return {
        "status": True,
        "message": "Success data rendered",
        "data": data,
    }


def prepare_create_response(msg):
    return {
        "status": True,
        "message": msg,
    }
