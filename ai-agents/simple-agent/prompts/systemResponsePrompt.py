def systemResponsePrompt(
        systemResponses,
        actions,
        newMessages
):
    # System responses to the model previous query
    feedbackDesc = ""
    for response in systemResponses:
        feedbackDesc.join(f"{response}\r\n")

    # Current action plan made by the agent
    actionsDesc = "Current Actions:\r\n"
    i = 0
    for actionId, actionContent in actions.items():
        actionsDesc.join(f"{i}. {actionContent} ({actionId})\r\n")

    # New messages received asynchronously from the server
    messagesDesc = "New Messages:\r\n"
    for sender, messageContent in newMessages.items():
        messagesDesc.join(f"{sender}: {messageContent}\r\n")

    return feedbackDesc.join(f"{actionsDesc}\r\n").join(f"{messagesDesc}\r\n")