class JoinMenuContext:
    def __init__(self):
        self.active_simulations = {
            "Simulation1" : (2, 5),
            "Simulation2" :  (0, 3),
            "Simulation3" : (4, 8)
        }

        self.ai_agent_mode = False
        self.simulation_list = None

    def Return(self):
        print("Returned to the main menu!")

    def ReloadList(self):
        print("Drawn new data from the network and reloaded the list!")

    def SearchForSimulation(self, keyword):
        if self.simulation_list is None:
            return

        current_simulations = {}

        for name, player_status in self.active_simulations.items():
            if keyword in name:
                current_simulations[name] = player_status

        self.simulation_list.refresh_list(current_simulations)

    def ResetSimulationList(self):
        self.simulation_list.refresh_list(self.active_simulations)
