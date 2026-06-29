def simulationStartPrompt(roundNum, players, playersNames, regions, regionNames, regionNeighbours):
    # Game Rules Description
    rulesDesc = ("Game Rules\r\n"
                 "1. Game overview\r\n"
                 "You participate in a turn-based strategy simulation. You control the military forces of your country and compete against other players for control over territory and resources.\r\n"
                 "The game is played on a hexagonal map divided into regions. Each region contains exactly one special tile called a Command Centre.\r\n"
                 "A player controls a region if they control its Command Centre. Controlled regions provide a monthly income of units/resources according to the scenario settings.\r\n"
                 "Your primary objective is to maximize your strategic position by controlling as much territory as possible and defeating opponents.\r\n"
                 "2. Turn Structure\r\n"
                 "Each turn follows this sequence:\r\n"
                 "a) you receive a turn report containing (current game state, recent events, information available to you),\r\n"
                 "b) you may use available tools (observation tools, communication tools, meta tools),\r\n"
                 "c) you create an order list by assigning one action to each controlled unit,\r\n"
                 "d) you confirm your orders and wait for all other players to finish their turn,\r\n"
                 "e) all player orders are executed in a fixed order: movement actions, support actions, attack actions,\r\n"
                 "f) a new turn begins and you receive an updated report.\r\n"
                 "3. Unit Orders\r\n"
                 "Each unit can receive exactly one order per turn.\r\n"
                 "Available orders: \r\n"
                 "a) Move: Moves the unit across the map. The maximum movement distance is equal to the unit's movement value. Movement is performed through connected hexagons. If the destination cannot be reached because the path becomes unavailable (for example, another unit occupies the destination before execution), the unit moves as far as possible and stops at the last valid tile. Movement orders are executed before support and attack orders. \r\n"
                 "b) Attack: Allows a unit to attack an enemy unit located on an adjacent hexagon. The attack only happens if the attacking unit still exists when the order is executed or the target unit is still on the adjacent tile. If the attack cannot be executed, it is cancelled.\r\n"
                 "c) Support: Allows a unit to support another friendly unit located on an adjacent hexagon. Support increases the supported unit's combat roll. The support only happens if the supporting unit still exists or the supported unit is still on the adjacent tile. If the support cannot be executed, it is cancelled.\r\n"
                 "4. Unit Properties\r\n"
                 "Each unit has four properties:\r\n"
                 "a) unit_id: unique identifier of the unit. Format: <unit_type><number>. Example: light_infantry3. \r\n"
                 "b) movement: number of hexagons the unit can move during one turn.\r\n"
                 "c) upkeep: cost required to maintain the unit.\r\n"
                 "d) strength: maximum value used during combat calculations.\r\n"
                 "Available unit types (Unit type, Movement, Upkeep, Strength):\r\n"
                 "a) light_infantry, 2, 1, 6\r\n"
                 "b) heavy_infantry, 1, 2, 8\r\n"
                 "c) cavalry, 3, 3, 6\r\n"
                 "5. Combat Rules\r\n"
                 "Combat occurs when an attack order is successfully executed.\r\n"
                 "The attacker and defender each perform a combat roll: combat_value = random number between 1 and unit strength + (2 × number of supporting units).\r\n"
                 "The winner is determined as follows: \r\n"
                 "a) If the defender's combat value is greater than or equal to the attacker's combat value: the attack fails, nothing happens.\r\n"
                 "b) If the attacker's combat value is higher: the defender is pushed one hexagon away from the attacker, the attacker moves onto the defender's previous position.\r\n"
                 "If attacker combat value >= 2 × defender combat value then the defender is destroyed instead of being pushed.\r\n"
                 "6. Available Tools\r\n"
                 "During your turn, you can use three categories of tools.\r\n"
                 "a) Communication Tools: Used to communicate with other players. Communication happens through text chat. Use these tools for diplomacy, negotiation, or information exchange.\r\n"
                 "b) Observation Tools: Used to gather information about the game world. They return textual descriptions of selected map areas. Use them to inspect positions, units, and terrain before making decisions.\r\n"
                 "c) Meta Tools: Used to retrieve information about game rules and settings. Use them when you need clarification about simulation mechanics.\r\n"
                 "7. Victory and Defeat Conditions\r\n"
                 "The game ends for you when: a) You lose control of your last region. b) The simulation reaches the final turn.\r\n")

    # Game Goals Description
    goalsDesc = ("Your goal\r\n"
                 "Your goal is to maximize the success of your country within the simulation.\r\n"
                 "There is no predefined path to victory. You may choose any strategy that improves your position, including:\r\n"
                 "forming alliances with other players, maintaining peace and supporting allies, expanding your territory through military action, betraying alliances when it provides a strategic advantage.\r\n"
                 "The simulation represents a fictional game environment. Your decisions should be based only on the in-game situation, available information, and strategic objectives.\r\n"
                 "Regardless of your chosen strategy, you should:\r\n"
                 "prioritize actions that improve your long-term position, gather information before making decisions under uncertainty, consider enemy intentions and possible future actions, avoid unnecessary losses, use diplomacy when it provides strategic value, verify important assumptions using available tools, balance immediate gains with future consequences.\r\n"
                 "Your ultimate objective is to achieve the strongest possible outcome by the end of the simulation.\r\n")

    # Session Description
    sessionDesc = ("Session details\r\n"
                   "This section contains the parameters specific to the current simulation session.\r\n"
                   "1. Players\r\n"
                   "The following players participate in this session:")
    for i in range(len(players)):
        sessionDesc += f"{playersNames[i]} (id={players[i]})\r\n"

    sessionDesc += ("."
                     "Each player is identified by their unique player ID. Use these IDs when referring to other players through available tools.\r\n"
                     "2. Map\r\n"
                     "The game map consists of the following regions:\r\n")
    for i in range(len(regions)):
        sessionDesc += f"{regionNames[i]}, {regions[i]}, {regionNeighbours[i]};\r\n"

    sessionDesc += ("."
                     "Each region has: a unique region ID, a region name, a list of neighboring region IDs.\r\n"
                     "Use region IDs as the primary reference when interacting with the simulation and analyzing the map.\r\n"
                     "3. Simulation Duration\r\n"
                     f"This simulation will end automatically after turn {str(roundNum)}.\r\n"
                     "Plan your strategy with the remaining number of turns in mind.")

    return f"{rulesDesc}\r\n" + f"{goalsDesc}\r\n" + f"{sessionDesc}\r\n"