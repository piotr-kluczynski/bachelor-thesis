from langchain.tools import tool

# Diplomacy tools
@tool
def sendMessage(playerId: int, content: str) -> str:
    """
    Sends message to the player with the given ID.

    :param playerId: ID of the target player.
    :param content: Content to send.
    :return: System response to the message.
    """

    # Sending message to the player using local communication.

    return "Message was sent successfully."


# Simulation tools
@tool
def moveUnit(unitID: int, moveQ: int, moveR: int, moveS: int) -> str:
    """
    Orders the unit with the given ID to move by the change vector defined by (moveQ, moveR, moveS).

    :param unitID: ID of the unit executing the order.
    :param moveQ: Change of the unit position in the direction q.
    :param moveR: Change of the unit position in the direction r.
    :param moveS: Change of the unit position in the direction s.
    :return: System response to the movement order.
    """

    # Verifying the validity of movement action locally
    # Saving the movement action to be sent with the rest of the orders

    return "Move order was added successfully."

@tool
def supportUnit(unitId: int, targetUnitId: int) -> str:
    """
    Orders the unit with unit ID to support the unit with target unit ID.

    :param unitId: ID of the unit executing the order.
    :param targetUnitId: ID of the supported unit.
    :return: System response to the support order.
    """

    # Verify the validity of the support action locally
    # Saving the support order to be sent with the rest of the orders

    return "Support order was added successfully."

@tool
def attackUnit(unitId: int, targetUnitId: int) -> str:
    """
    Orders the unit with unit ID to attack the unit with target unit ID.

    :param unitId: ID of the unit executing the order.
    :param targetUnitId: ID of the attacked unit.
    :return: System response to the attack order.
    """

    # Verify the validity of the attack action locally
    # Saving the attack order to be sent with the rest of the orders

    return "Attack order was added successfully."


# Observation tools
@tool
def observeUnit(unitId: int) -> str:
    """
    Returns the terrain around unit with given unit ID.
    In case of failure, returns an error message instead.

    :param unitId: ID of the target unit.
    :return: Description of the terrain around unit.
    """

    # Verify the validity of the tool call locally
    # Local copy of the application returns the terrain description.

    return "<Terrain description>"

@tool
def observeRegion(regionId: int) -> str:
    """
    Returns the terrain belonging to the region with given region ID.

    :param regionId: ID of the target region.
    :return: Description of the terrain belonging to the region.
    """

    # Verify the validity of the tool call locally
    # Local copy of the application returns the terrain description

    return "<Terrain description>"


# Meta tools

# Think about adding the tools describing the game rules,
# so that the model can recall some specific mechanics at any time
@tool
def finishTurn():
    """
    Finishes the current turn.

    :return:
    """

@tool
def playerList() -> str:
    """
    Returns the list of remaining players.

    # Draw the player list from the local version of the simulation.

    :return: "<List of remaining players>"
    """

@tool
def leaderBoard() -> str:
    """
    Returns the leaderboard.

    :return: List of all players and their positions on the leaderboard.
    """

    # Draws data from the local version of the app.

    return "<Leaderboard>"

@tool
def controlledUnits() -> str:
    """
    Returns the list of owned units.

    :return: List of owned units.
    """

    # Get list of units from the local version of the simulation.
    return "<Owned units>"

@tool
def unitDetails(unitId: int) -> str:
    """
    Returns the details of the given unit ID.

    :param unitId: ID of the unit.
    :return: Description of the unit.
    """

    # Draw data about the unit from the local version of the app.

    return "<Unit details>"

@tool
def controlledRegions() -> str:
    """
    Returns the list of owned regions.

    :return: List of owned regions.
    """

    return "<List of owned regions>"

@tool
def mapDescription() -> str:
    """
    Returns the description of the map.

    :return: List of all regions of the map.
    """

    # Draw description of all regions of the map.

    return "<Map description>"

@tool
def getRecentEvents() -> str:
    """
    Recovers the recent events from this turn report.

    :return: Description of the recent events.
    """

    return "<Recent events>"

@tool
def getConversation(userId: int) -> str:
    """
    Gets the conversation with the given user ID.

    :param userId: ID of the player who was conversing with the user.
    :return: Conversation content.
    """

    return "<Conversation content>"