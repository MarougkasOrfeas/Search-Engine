class NoPapersFoundException(Exception):
    def __init__(self, message="No papers found for the given query."):
        self.message = message
        super().__init__(self.message)
