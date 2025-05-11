import discord


def formatEmbed(gameData : dict) -> discord.Embed:
    '''returns a formatted embed of a turn'''
    print(gameData)
    match gameData.get("outcome"):
        case "DEALER_WINS":
            title = "Dealer Wins"
        case "PLAYER_WINS":
            title = "Player Wins"
        case "PUSH":
            title = "Draw, No One Wins"
        case __:
            title = "Unresolved Game"
    embedVar = discord.Embed(title=title, color=0x00ff00)   
    embedVar.add_field(name="Dealer: ", value=f"Cards: {gameData.get("dealerCards")} | Value: {str(gameData.get("dealerValue"))}")
    for i in range(2): # adds blank spaces
        embedVar.add_field(name='\u200b', value='\u200b', inline=False)
    embedVar.add_field(name="Player: ", value=f"Cards: {gameData.get("playerCards")} | Value: {str(gameData.get("playerValue"))}")
    embedVar.set_footer(text=f"Balance: {str(gameData.get("balance"))} | Bet: {str(gameData.get("currentBet"))} | Cards Remaining: {str(gameData.get("cardsRemaining"))} ")
    
    return embedVar

