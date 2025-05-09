import logging
from datetime import date
from pathlib import Path


class StickLogger(logging.Logger):
    def __init__(self):
        """
        Initialize the logger.

        This logger will log at the INFO level by default. The log file will be
        saved in the "logs" directory and will be named after the current date.

        The log file will be created if it does not already exist.

        The logger will also log to the console.

        :return: None
        """
        
        super().__init__(
            name="StickLogger",
            level=logging.INFO,
        )
        self.date = date.today()
        self.log_file = Path(f"logs/{self.date}.log")
        self.log_file.touch()

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s     %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
        self.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s     %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
        self.addHandler(console_handler)
        
    def log_info(self, message):
        """
        Log an informational message.

        This method logs a message at the INFO level. The message will be
        recorded in the log file and printed to the console.

        Parameters:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.info(message)
    
    def log_warning(self, message):
        """
        Log a warning message.

        This method logs a message at the WARNING level. The message will be
        recorded in the log file and printed to the console.

        Parameters:
            message (str): The message to be logged.

        Returns:
            None
        """

        self.warning(message)
    
    def log_error(self, message):
        """
        Log an error message.

        This method logs a message at the ERROR level. The message will be
        recorded in the log file and printed to the console.

        Parameters:
            message (str): The message to be logged.

        Returns:
            None
        """
        self.error(message)