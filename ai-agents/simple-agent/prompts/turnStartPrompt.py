def turnStartPrompt(
        currentRound, finalRound, playerList, leaderBoardDict,
        controlledUnits, controlledRegions, enemyUnitsPerRegion,
        eventDict):

    # Game State
    gameStateDesc = (f"Round {currentRound}/{finalRound}"
                     "Remaining players:\r\n")
    for player in playerList:
        gameStateDesc.join(player)

    gameStateDesc.join("Leaderboard:\r\n")
    i = 0
    for player, score in leaderBoardDict.items():
        gameStateDesc.join(f"{i}. {player}: {score}\r\n")
        i += 1

    # Military Overview
    militaryDesc = "Controlled Units:\r\n"
    for unit in controlledUnits:
        militaryDesc.join(f"{unit}\r\n")

    militaryDesc.join("Controlled Regions:\r\n")
    for regionId, regionName in controlledRegions.items():
        militaryDesc.join(f"{regionName}({regionId}), enemy units in the region: {enemyUnitsPerRegion[regionId]}\r\n")


    # Events
    eventsDesc = ""
    for eventTitle, eventContent in eventDict.items():
        eventsDesc.join(f"{eventTitle}: {eventContent}\r\n")

    return gameStateDesc.join(f"{militaryDesc}\r\n").join(f"{militaryDesc}\r\n")