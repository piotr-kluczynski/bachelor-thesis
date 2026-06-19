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


# Meta tools - Expand for better game-state analysis
@tool
def gameState() -> str:
    """
    Recovers the game state from this turn report.

    :return: Description of the game state.
    """

    return "<Game state>"

@tool
def militaryOverview() -> str:
    """
    Recovers the military overview from this turn report.

    :return: Description of the military overview.
    """

    return "<Military overview>"

@tool
def recentEvents() -> str:
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

