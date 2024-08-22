import sys
import traceback

def error_message_detail(error, error_detail: sys):
    # Get the exception information from sys.exc_info()
    _, _, exc_tb = error_detail.exc_info()
    
    if exc_tb is not None:
        # If traceback is available, extract file name and line number
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            file_name, exc_tb.tb_lineno, str(error)
        )
    else:
        # If traceback is not available, use a generic error message
        error_message = "Error message: [{0}]".format(str(error))
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys = None):
        super().__init__(error_message)
        if error_detail:
            self.error_message = error_message_detail(error_message, error_detail)
        else:
            # If no error detail is provided, use a simpler error message
            self.error_message = error_message

    def __str__(self):
        return self.error_message
