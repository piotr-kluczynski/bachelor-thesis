from players.PlayerStrategy import PlayerStrategy


class DebugMode(PlayerStrategy):
    def __init__(self, tools):
        self.tools = tools
        self.conversation = []
        self.lastResponse = None

    def initializePlayer(self):
        print("Initializing player")

    def simulationStart(self, simulationStartMessage):
        print(simulationStartMessage)

    def simulationEnd(self):
        print("Simulation ended")

    def roundStart(self, roundStartMessage):
        print(roundStartMessage)

    def roundEnd(self):
        print("Round ended")

    def turnStart(self):
        while True:
            print("Turn started!")
            print("Choose the tool to use (-1 to exit):")

            for i, tool in enumerate(self.tools):
                print(f"{i}. {tool.name}")

            decision = int(input("> "))

            if decision == -1:
                break

            selected_tool = self.tools[decision]

            print(f"\nSelected tool: {selected_tool.name}")
            print(selected_tool.description)

            arguments = {}

            for arg_name, arg_info in selected_tool.args.items():
                value = input(f"Enter {arg_name}: ")

                arg_type = arg_info.get("type")

                if arg_type == "integer":
                    value = int(value)
                elif arg_type == "number":
                    value = float(value)
                elif arg_type == "boolean":
                    value = value.lower() in ["true", "1", "yes"]

                arguments[arg_name] = value

            result = selected_tool.invoke(arguments)

            print("Tool executed:", result)


    def turnEnd(self, turnEndMessage):
        print(turnEndMessage)