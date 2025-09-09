import datetime

class CustomLogger:
    def __init__(self, file_path='app.log'):
        self.file_path = file_path

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().isoformat()
        log_message = f"{timestamp} - {level} - {message}\n"
        with open(self.file_path, "a") as log_file:
            log_file.write(log_message)