from langchain.tools import tool

used_actions = []

# Diplomacy tools
@tool
def sendMessage(playerId: int, content: str):
    """
    Sends message to the player with the given ID.

    :param playerId: ID of the target player.
    :param content: Content to send.
    """

    used_actions.append(
        {
            "Action" : "SendMessage",
            "PlayerId" : playerId,
            "Content" : content
        }
    )


# Simulation tools
@tool
def moveUnit(unitID: int, moveQ: int, moveR: int, moveS: int):
    """
    Orders the unit with the given ID to move by the change vector defined by (moveQ, moveR, moveS).

    :param unitID: ID of the unit executing the order.
    :param moveQ: Change of the unit position in the direction q.
    :param moveR: Change of the unit position in the direction r.
    :param moveS: Change of the unit position in the direction s.
    """

    used_actions.append(
        {
            "Action" : "MoveUnit",
            "UnitID" : unitID,
            "MoveQ" : moveQ,
            "MoveR" : moveR,
            "MoveS" : moveS
        }
    )

@tool
def supportUnit(unitId: int, targetUnitId: int):
    """
    Orders the unit with unit ID to support the unit with target unit ID.

    :param unitId: ID of the unit executing the order.
    :param targetUnitId: ID of the supported unit.
    """

    used_actions.append(
        {
            "Action" : "SupportUnit",
            "UnitID" : unitId,
            "TargetUnitID" : targetUnitId
        }
    )

@tool
def attackUnit(unitId: int, targetUnitId: int):
    """
    Orders the unit with unit ID to attack the unit with target unit ID.

    :param unitId: ID of the unit executing the order.
    :param targetUnitId: ID of the attacked unit.
    """

    used_actions.append(
        {
            "Action" : "AttackUnit",
            "UnitID" : unitId,
            "TargetUnitID" : targetUnitId
        }
    )


# Observation tools
@tool
def observeUnit(unitId: int):
    """
    Returns the terrain around unit with given unit ID.
    In case of failure, returns an error message instead.

    :param unitId: ID of the target unit.
    """

    used_actions.append(
        {
            "Action" : "ObserveUnit",
            "UnitID" : unitId
        }
    )

@tool
def observeRegion(regionId: int):
    """
    Returns the terrain belonging to the region with given region ID.

    :param regionId: ID of the target region.
    """

    used_actions.append(
        {
            "Action" : "ObserveRegion",
            "RegionID" : regionId
        }
    )


# Meta tools

# Think about adding the tools describing the game rules,
# so that the model can recall some specific mechanics at any time
@tool
def finishTurn():
    """
    Finishes the current turn.
    """

    used_actions.append(
        {
            "Action" : "FinishTurn"
        }
    )

@tool
def playerList():
    """
    Returns the list of remaining players.

    # Draw the player list from the local version of the simulation.

    """

    used_actions.append(
        {
            "Action" : "PlayerList"
        }
    )

@tool
def leaderBoard():
    """
    Returns the leaderboard.

    """

    used_actions.append(
        {
            "Action" : "LeaderBoard"
        }
    )

@tool
def controlledUnits():
    """
    Returns the list of owned units.

    """

    used_actions.append(
        {
            "Action" : "ControlledUnits"
        }
    )


@tool
def unitDetails(unitId: int):
    """
    Returns the details of the given unit ID.

    :param unitId: ID of the unit.
    """

    used_actions.append(
        {
            "Action" : "UnitDetails",
            "UnitID" : unitId
        }
    )


@tool
def controlledRegions():
    """
    Returns the list of owned regions.

    """

    used_actions.append(
        {
            "Action" : "ControlledRegions"
        }
    )

@tool
def mapDescription():
    """
    Returns the description of the map.
    """

    used_actions.append(
        {
            "Action" : "MapDescription"
        }
    )

@tool
def getRecentEvents():
    """
    Recovers the recent events from this turn report.
    """

    used_actions.append(
        {
            "Action" : "GetRecentEvents"
        }
    )

@tool
def getConversation(userId: int):
    """
    Gets the conversation with the given user ID.

    :param userId: ID of the player who was conversing with the user.
    """

    used_actions.append(
        {
            "Action" : "GetConversation",
            "UserID" : userId
        }
    )