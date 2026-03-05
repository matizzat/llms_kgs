import logging

logging.basicConfig(filename="./logfile.log", format='%(asctime)s %(message)s', filemode='a')

logger = logging.getLogger()

def log_error(class_name: str, method_name: str, e: Exception):
    error_message = """
    <Error at {method_name} in class {class_name}>\n
    (Exception)
    @
    {e}
    @
    """.format(
            method_name = method_name,
            class_name = class_name,
            e = str(e))
    logger.error(error_message)
