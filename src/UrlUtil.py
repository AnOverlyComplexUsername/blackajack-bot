import os
from typing import Final
from dotenv import load_dotenv
import requests

#helper for parsing URL strings 
load_dotenv()
USER : Final[str] = os.getenv('USER')
PASS : Final[str] = os.getenv('PASSWORD')
sesID : str = None
__API_START : str = "http://euclid.knox.edu:8080/api/blackjack/"
__API_END : str = f"?username={USER}&password={PASS}"
#http://euclid.knox.edu:8080/api/blackjack/sessions/vtang?password=3fe1c42

def setGameID(id : str):
    '''sets current game id'''
    global sesID
    sesID = id

def resetGame():
    return requests.post(URLBuilder(f"{sesID}/reset"))

def stand():
    return requests.post(URLBuilder(f"{sesID}/stand" ))

def hit():
    return requests.post(URLBuilder(f"{sesID}/hit"))

def finishGame():
    return requests.post(URLBuilder(f"{sesID}/finish"))

def bet(amount : int):
    print(sesID)
    return requests.post(URLBuilder(f"{sesID}/bet/{amount}"))

def startGame():
    return requests.post(URLBuilder("start"))

def resumeGame():
    return requests.post(URLBuilder(f"resume/{sesID}"))

def getGameState():
    return requests.get(URLBuilder(f"{sesID}/state"))

def getGameSessions():
    return requests.get(__API_START + f"sessions/{USER}?password={PASS}")

def getCurSessions():
    return requests.get(URLBuilder("my-session"))

            
def URLBuilder(action : str) -> str:
    return __API_START + action + __API_END
        