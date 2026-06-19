def simulationStartPrompt(roundNum, playerList, regionNames, regionNeighbours):
    # Game Rules Description
    rulesDesc = ("Game Rules"
                 "1. Game overview"
                 "You participate in a turn-based strategy simulation. You control the military forces of your country and compete against other players for control over territory and resources."
                 "The game is played on a hexagonal map divided into regions. Each region contains exactly one special tile called a Command Centre."
                 "A player controls a region if they control its Command Centre. Controlled regions provide a monthly income of units/resources according to the scenario settings."
                 "Your primary objective is to maximize your strategic position by controlling as much territory as possible and defeating opponents."
                 "2. Turn Structure"
                 "Each turn follows this sequence:"
                 "a) you receive a turn report containing (current game state, recent events, information available to you),"
                 "b) you may use available tools (observation tools, communication tools, meta tools),"
                 "c) you create an order list by assigning one action to each controlled unit,"
                 "d) you confirm your orders and wait for all other players to finish their turn,"
                 "e) all player orders are executed in a fixed order: movement actions, support actions, attack actions,"
                 "f) a new turn begins and you receive an updated report."
                 "3. Unit Orders"
                 "Each unit can receive exactly one order per turn."
                 "Available orders: "
                 "a) Move: Moves the unit across the map. The maximum movement distance is equal to the unit's movement value. Movement is performed through connected hexagons. If the destination cannot be reached because the path becomes unavailable (for example, another unit occupies the destination before execution), the unit moves as far as possible and stops at the last valid tile. Movement orders are executed before support and attack orders. "
                 "b) Attack: Allows a unit to attack an enemy unit located on an adjacent hexagon. The attack only happens if the attacking unit still exists when the order is executed or the target unit is still on the adjacent tile. If the attack cannot be executed, it is cancelled."
                 "c) Support: Allows a unit to support another friendly unit located on an adjacent hexagon. Support increases the supported unit's combat roll. The support only happens if the supporting unit still exists or the supported unit is still on the adjacent tile. If the support cannot be executed, it is cancelled."
                 "4. Unit Properties"
                 "Each unit has four properties:"
                 "a) unit_id: unique identifier of the unit. Format: <unit_type><number>. Example: light_infantry3. "
                 "b) movement: number of hexagons the unit can move during one turn."
                 "c) upkeep: cost required to maintain the unit."
                 "d) strength: maximum value used during combat calculations."
                 "Available unit types (Unit type, Movement, Upkeep, Strength):"
                 "a) light_infantry, 2, 1, 6"
                 "b) heavy_infantry, 1, 2, 8"
                 "c) cavalry, 3, 3, 6"
                 "5. Combat Rules"
                 "Combat occurs when an attack order is successfully executed."
                 "The attacker and defender each perform a combat roll: combat_value = random number between 1 and unit strength + (2 × number of supporting units)."
                 "The winner is determined as follows: "
                 "a) If the defender's combat value is greater than or equal to the attacker's combat value: the attack fails, nothing happens."
                 "b) If the attacker's combat value is higher: the defender is pushed one hexagon away from the attacker, the attacker moves onto the defender's previous position."
                 "If attacker combat value >= 2 × defender combat value then the defender is destroyed instead of being pushed."
                 "6. Available Tools"
                 "During your turn, you can use three categories of tools."
                 "a) Communication Tools: Used to communicate with other players. Communication happens through text chat. Use these tools for diplomacy, negotiation, or information exchange."
                 "b) Observation Tools: Used to gather information about the game world. They return textual descriptions of selected map areas. Use them to inspect positions, units, and terrain before making decisions."
                 "c) Meta Tools: Used to retrieve information about game rules and settings. Use them when you need clarification about simulation mechanics."
                 "7. Victory and Defeat Conditions"
                 "The game ends for you when: a) You lose control of your last region. b) The simulation reaches the final turn.")

    # Game Goals Description
    goalsDesc = ("Your goal"
                 "Your goal is to maximize the success of your country within the simulation."
                 "There is no predefined path to victory. You may choose any strategy that improves your position, including:"
                 "forming alliances with other players, maintaining peace and supporting allies, expanding your territory through military action, betraying alliances when it provides a strategic advantage."
                 "The simulation represents a fictional game environment. Your decisions should be based only on the in-game situation, available information, and strategic objectives."
                 "Regardless of your chosen strategy, you should:"
                 "prioritize actions that improve your long-term position, gather information before making decisions under uncertainty, consider enemy intentions and possible future actions, avoid unnecessary losses, use diplomacy when it provides strategic value, verify important assumptions using available tools, balance immediate gains with future consequences."
                 "Your ultimate objective is to achieve the strongest possible outcome by the end of the simulation.")

    # Session Description
    sessionDesc = ("Session details"
                   "This section contains the parameters specific to the current simulation session."
                   "1. Players"
                   "The following players participate in this session:")
    for player in playerList:
        sessionDesc.join(player)

    sessionDesc.join("."
                     "Each player is identified by their unique player ID. Use these IDs when referring to other players through available tools."
                     "2. Map"
                     "The game map consists of the following regions:")
    for regionId, regionName in regionNames.items():
        neighbours = regionNeighbours[regionId]
        sessionDesc.join(f"{regionName}, {regionId}, {neighbours};")

    sessionDesc.join("."
                     "Each region has: a unique region ID, a region name, a list of neighboring region IDs."
                     "Use region IDs as the primary reference when interacting with the simulation and analyzing the map."
                     "3. Simulation Duration"
                     f"This simulation will end automatically after turn {str(roundNum)}."
                     "Plan your strategy with the remaining number of turns in mind.")

    return rulesDesc.join(f"{goalsDesc}\r\n").join(f"{sessionDesc}\r\n")