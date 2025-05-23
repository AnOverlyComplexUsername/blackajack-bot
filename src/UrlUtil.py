import os
from typing import Final
from dotenv import load_dotenv
import requests

'''wrapper functions for interacting w/ blackjack server'''

load_dotenv()
USER : Final[str] = os.getenv('USER')
PASS : Final[str] = os.getenv('PASSWORD')
sesID : str = None
__API_START : str = "http://euclid.knox.edu:8080/api/blackjack/"
__API_END : str = f"?username={USER}&password={PASS}"

def setGameID(id : str):
    '''sets current game id'''
    global sesID
    sesID = id

def resetGame():
    return requests.post(URLBuilder(f"{sesID}/reset"))

def stand()  -> dict:
    return requests.post(URLBuilder(f"{sesID}/stand" )).json()

def hit() -> dict:
    return requests.post(URLBuilder(f"{sesID}/hit")).json()

def finishGame():
    return requests.post(URLBuilder(f"{sesID}/finish"))

def bet(amount : int) -> dict:
    return requests.post(URLBuilder(f"{sesID}/bet/{amount}")).json()

def startGame():
    return requests.post(URLBuilder("start"))

def resumeGame():
    ''' takes a session id and reusmes playing in that session'''
    return requests.post(URLBuilder(f"resume/{sesID}"))

def getGameState() -> dict:
    return requests.get(URLBuilder(f"{sesID}/state")).json()

def getGameSessions():
    return requests.get(__API_START + f"sessions/{USER}?password={PASS}").json()

def getCurSessions():
    return requests.get(URLBuilder("my-session"))

            
def URLBuilder(action : str) -> str:
    '''helper for parsing URL strings'''
    return __API_START + action + __API_END
        