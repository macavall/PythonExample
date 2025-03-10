import azure.functions as func
import logging
from cffi import FFI

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Create an instance of FFI
ffi = FFI()

# Define the function prototype and load the shared library
ffi.cdef("int add(int, int);")
C = ffi.dlopen("./my_c_code.dll")  # Path to the compiled shared library

@app.route(route="http1")
def http1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Example usage of the C function
    result = C.add(10, 20)  # Call the C function
    
    logging.info(result)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. C function result: {result}")
    else:
        return func.HttpResponse(
            f"This HTTP triggered function executed successfully. C function result: {result}. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
