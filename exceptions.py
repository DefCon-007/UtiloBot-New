class BaseFunctionalityException(Exception): 
    def __init__(self, return_msg):
        self.return_msg = return_msg
        pass

class InvalidSongURLException(BaseFunctionalityException): 
    def __init__(self):
        return_msg = "Invalid or no song URL supplied. Please add the URL alongwith command!"
        super().__init__(return_msg)


class CannotConvertSongException(BaseFunctionalityException): 
    def __init__(self):
        return_msg = "Unable to convert the given song. Please try again later!"
        super().__init__(return_msg)