class СhangeError(Exception):
    def __init__(self):
        message = "It is forbidden to change the config value"
        super().__init__(message)