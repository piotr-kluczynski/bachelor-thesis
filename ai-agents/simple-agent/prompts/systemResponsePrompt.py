def systemResponsePrompt(
        systemResponses,
        actions,
        newMessages
):
    # System responses to the model previous query
    feedbackDesc = ""
    for response in systemResponses:
        feedbackDesc += f"{response}\r\n"

    # Current action plan made by the agent
    actionsDesc = "Current Actions:\r\n"
    i = 0
    for actionId, actionContent in actions.items():
        actionsDesc += f"{i}. {actionContent} ({actionId})\r\n"

    # New messages received asynchronously from the server
    messagesDesc = "New Messages:\r\n"
    for sender, messageContent in newMessages.items():
        messagesDesc += f"{sender}: {messageContent}\r\n"

    return f"{feedbackDesc}\r\n" + f"{actionsDesc}\r\n" + f"{messagesDesc}\r\n"