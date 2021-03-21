class BaseFunctionalityException(Exception): 
    def __init__(self, return_msg):
        self.return_msg = return_msg
        pass
    
    
# /* TelegramParseCallbackQueryData exception start 

class InvalidCallbackQueryCategoryException(BaseFunctionalityException): 
    def __init__(self, category, return_msg=None):
        if not return_msg:
            return_msg = "Invalid category - {} in the callback data. Please try again!"
        super().__init__(return_msg)  

# TelegramParseCallbackQueryData exception end */

# /* SongParser exceptions start
class InvalidSongURLException(BaseFunctionalityException): 
    def __init__(self, return_msg=None):
        if not return_msg:
            return_msg = "Invalid or no song URL supplied. Please add the song URL along with the command!"
        super().__init__(return_msg)


class CannotConvertSongException(BaseFunctionalityException): 
    def __init__(self, return_msg=None):
        if not return_msg:
            return_msg = "Unable to convert the given song. Please try again later!"
        super().__init__(return_msg)
    
# SongeParser exceptions end */ 

# /* Jokes exception start    
class InvalidChuckNorrisJokeCategoryException(BaseFunctionalityException): 
    def __init__(self, return_msg=None):
        if not return_msg:
            return_msg = "Invalid category supplied for the Chuck Norris joke."
        super().__init__(return_msg)

class InvalidJokeTypeException(BaseFunctionalityException):
    def __init__(self, joke_type, return_msg=None):
        if not return_msg:
            return_msg = "Invalid joke type - {} received. Please try later!".format(joke_type)
        super().__init__(return_msg)
# Jokes exception end */

# /* URLShortner exception start

class UnableToShortenURLException(BaseFunctionalityException): 
    def __init__(self, return_msg=None):
        if not return_msg:
            return_msg = "Unable to shorten the URL. Please try again!"
        super().__init__(return_msg)

class NoURLToShortenException(BaseFunctionalityException): 
    def __init__(self, return_msg=None):
        if not return_msg:
            return_msg = "No URL found to shorten. Please try again!"
        super().__init__(return_msg)
# URLShortner exception end */
