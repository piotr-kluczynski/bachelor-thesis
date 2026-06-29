def roundStartPrompt(
        currentRound, finalRound, players, playerNames, leaderBoardDict,
        controlledUnits, controlledRegionsId, controlledRegionsNames, enemyUnitsPerRegion,
        eventDict):

    # Game State
    gameStateDesc = (f"Round {currentRound}/{finalRound[0]}\r\n"
                     "Remaining players:\r\n")
    for i in range(len(players)):
        gameStateDesc += f"{playerNames[i]} (id={players[i]})\r\n"

    gameStateDesc += f"Leaderboard:\r\n"
    i = 0
    for player, score in leaderBoardDict.items():
        gameStateDesc += f"{i}. {player}: {score}\r\n"
        i += 1

    # Military Overview
    militaryDesc = "Controlled Units:\r\n"
    for unit in controlledUnits:
        militaryDesc += f"{unit}\r\n"

    militaryDesc += "\r\nControlled Regions:\r\n"
    for i in range(len(controlledRegionsId)):
        militaryDesc += f"{controlledRegionsNames[i]}({controlledRegionsId[i]}), enemy units in the region: {enemyUnitsPerRegion[i]}\r\n"


    # Events
    eventsDesc = ""
    for eventTitle, eventContent in eventDict.items():
        eventsDesc += f"{eventTitle}: {eventContent}\r\n"

    return gameStateDesc + f"{militaryDesc}\r\n" + f"{eventsDesc}\r\n"