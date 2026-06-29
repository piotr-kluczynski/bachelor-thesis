from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from players.PlayerStrategy import PlayerStrategy


class SimpleAgent(PlayerStrategy):
    def __init__(self, model_version, tools):
        self.tools = tools
        self.conversation = []
        self.model_version = model_version

        self.lastResponse = None
        self.model = None
        self.agent = None

    def initializePlayer(self):
        api_key = input("Enter your API key: ")

        self.model = ChatOpenAI(
            model="gpt-4.1-mini",
            api_key=api_key,
        )

        self.agent = create_agent(
            model=self.model,
            tools=self.tools
        )

    def simulationStart(self, simulationStartMessage):
        self.conversation.append(
            SystemMessage(
                content=simulationStartMessage
            )
        )

    def simulationEnd(self):
        pass

    def roundStart(self, roundStartMessage):
        if roundStartMessage:
            self.conversation.append(
                SystemMessage(
                    content=roundStartMessage
                )
            )

    def roundEnd(self):
        pass

    def turnStart(self):
        self.lastResponse = self.agent.invoke(conversation=self.conversation)

    def turnEnd(self, turnEndMessage):
        self.conversation.append(AIMessage(content=self.lastResponse))
        self.conversation.append(SystemMessage(content=turnEndMessage))