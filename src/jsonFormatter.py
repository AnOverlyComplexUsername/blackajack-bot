import discord

'''formats game data jsons into Discord embeds'''

def formatSessionsEmbed(sessions : list[dict], startIndex : int = 0, entryRange: int = 5) -> discord.Embed:
    '''returns a formatted embed of a list of sessions
        Parameters
        -----------
    sesList: :class:`list`
        dictionary of list of all sessions in a dictionary format   
    startIndex: :class:`int`
        first index that's at the top of the page 
    entryRange: :class:`int`
        how many entries should be in each page'''
    embedVar = discord.Embed(title=f"Active Sessions {str(startIndex + 1)} to {str(startIndex + entryRange)}", color=0x75b7ea)
    for i in range(entryRange):
        if startIndex + i >  sessions.__len__() - 1 :
            break
        embedVar.add_field(name=f"Session {startIndex + i + 1}, ID:", value=sessions[startIndex+i].get("sessionId") + f"\n Balance: " + str(sessions[startIndex + i].get("balance")), inline=False)
    return embedVar

def formatEmbed(gameData : dict, i : discord.Interaction) -> discord.Embed:
    '''returns a formatted embed of a turn
        Parameters
        -----------
    gameData: :class:`dict`
        dictionary containing JSON data of current game state
    i: :class:`Interaction`
        discord interaction that called formatEmbed, used to get the username of the one who started the interaction'''
    print(gameData)
    username = i.user.display_name
    match gameData.get("outcome"):
        case "DEALER_WINS":
            title = "Dealer Wins"
        case "PLAYER_WINS":
            title = f"{username} Wins"
        case "PUSH":
            title = "Draw, No One Wins"
        case __:
            title = "Blackjack"
    embedVar = discord.Embed(title=title, color=0x75b7ea)   
    embedVar.add_field(name="Dealer: ", value=f"Cards: {gameData.get("dealerCards")} | Value: {str(gameData.get("dealerValue"))}")
    for i in range(2): # adds blank spaces 
        embedVar.add_field(name='\u200b', value='\u200b', inline=False)
    embedVar.add_field(name=f"Player: {username}", value=f"Cards: {gameData.get("playerCards")} | Value: {str(gameData.get("playerValue"))}")
    embedVar.set_footer(text=f"Balance: {str(gameData.get("balance"))} | Bet: {str(gameData.get("currentBet"))} | Cards Remaining: {str(gameData.get("cardsRemaining"))} \nSession ID: {gameData.get("sessionId")}")
    
    return embedVar

