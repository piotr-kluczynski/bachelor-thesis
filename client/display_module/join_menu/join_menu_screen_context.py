class JoinMenuContext:
    def __init__(self):
        self.active_simulations = {
            "Simulation1" : (2, 5),
            "Simulation2" :  (0, 3),
            "Simulation3" : (4, 8)
        }

    def Return(self):
        print("Returned to the main menu!")