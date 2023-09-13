import datetime
from pymongo import MongoClient


def printman():
    s = '''  
            ## Available commands :
                `$add-me` -> Add user in database. [ nothing happens if user already added ]
                `$flag [id] [flag]` -> command for submitting flag. [ flag must be in format `njack{text}` ]
                                       this command is only accessible in private messgae/dm mode.
                `$show-leaderboards` -> show leaderboard. [ coming soon ]
                `$my-score` -> show your score. [ coming soon ]
                `$show-challenges` -> show active challange. 
        '''
    return(s)