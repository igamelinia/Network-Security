import sys
from networksecurity.logging import logger

class CustomException(Exception):
    def __init__(self, error_msg, error_detail:sys):
        self.error_msg = error_msg
        _,_,ext_tb = error_detail.exc_info()

        self.lineno = ext_tb.tb_lineno
        self.file_name = ext_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error in file [{self.file_name}] line number [{self.lineno}] error message [{self.error_msg}]"
    

# Check code
# if __name__=="__main__":
#     try:
#         logger.logging.info("Test Custome Exception and Logging")
#         a = 1/0
#         print("This will not be printed")

#     except Exception as e:
#         raise CustomException(e, sys)