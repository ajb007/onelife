def message(json, message):

    if not "messages" in json.keys():
        json["messages"] = []
    json["messages"].append(message)
    return

def broadcast(json, message):
    if not "broadcast" in json.keys():
        json["broadcast"] = []
    json["broadcast"].append(message)
    return
