import logging

class ExceptionLogger:
    @staticmethod
    def log_exception(e, context=""):
        length = len(context)
        stars = '*' * length
        marks = '!' * length
        logging.info("   "+stars)
        logging.info("   "+marks)
        logging.info("   "+context)
        exception_type = type(e).__name__
        logging.info(f"   {exception_type}: {e}")
        logging.exception("   Exception:")
        logging.info("   "+marks)
        logging.info("   "+stars)
