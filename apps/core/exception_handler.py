from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.get('data'):
            if response.data.get('detail'):
                response.data['message'] = response.data.pop('detail')
    
    return response