import os
from typing import Final
from dotenv import load_dotenv
import requests


load_dotenv()
USER : Final[str] = os.getenv('USER')
PASS : Final[str] = os.getenv('PASSWORD')
__API_START : str = "http://euclid.knox.edu:8080/api/blackjack/"
__API_END : str = f"?username={USER}&password={PASS}"

                
def URLBuilder(action : str) -> str:
    '''helper for parsing URL strings'''
    return __API_START + action + __API_END

def getGameSessions():
    return requests.get(__API_START + f"sessions/{USER}?password={PASS}").json()

class UrlUtil: 
    '''wrapper class for interacting w/ blackjack server'''
    sesID : str = None
    
    def __init__(self, id : str = None):
        ''' Parameters
        -----------
        id: :class:`str`  
            sessionID being used for current game
        '''
        if id:
            self.setGameID(id=id)
        
    def setGameID(self, id : str):
        '''sets current game ID'''
        self.sesID = id
    
    def getGameID(self): 
        '''gets current game ID'''
        return self.sesID

    def resetGame(self):
        return requests.post(URLBuilder(f"{self.sesID}/reset"))

    def stand(self)  -> dict:
        return requests.post(URLBuilder(f"{self.sesID}/stand" )).json()

    def hit(self) -> dict:
        return requests.post(URLBuilder(f"{self.sesID}/hit")).json()

    def finishGame(self):
        return requests.post(URLBuilder(f"{self.sesID}/finish"))

    def bet(self,amount : int) -> dict:
        return requests.post(URLBuilder(f"{self.sesID}/bet/{amount}")).json()

    def startGame(self):
        return requests.post(URLBuilder("start"))

    def resumeGame(self):
        ''' takes a session id and reusmes playing in that session'''
        return requests.post(URLBuilder(f"resume/{self.sesID}"))

    def getGameState(self) -> dict:
        return requests.get(URLBuilder(f"{self.sesID}/state")).json()

    def getCurSessions():
        return requests.get(URLBuilder("my-session"))


            