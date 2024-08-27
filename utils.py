def create_success_response(data):
    return {
        "status": "success",
        "data": data,
    }

def create_error_response(error):
    return { 
        "status": "error",
        "error": error,
    }

def create_response(error, data):
    if error :
        return create_error_response(error)
    else :
        return create_success_response(data)