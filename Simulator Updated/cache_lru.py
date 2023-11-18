from memory import memory_dict

sets = {
    "00": {"ru": None, "data": [None, None]},
    "01": {"ru": None, "data": [None, None]},
    "10": {"ru": None, "data": [None, None]},
    "11": {"ru": None, "data": [None, None]}
}

misses = 0
hits = 0


def update(addr, setno):
    global sets
    global misses
    global hits
    if sets[setno]["ru"] == None:
        # print("Miss")
        misses += 1
        sets[setno]["data"][0] = addr
        sets[setno]["ru"] = 0
    else:
        if addr in sets[setno]["data"]:
            # print("Hit")
            hits += 1
            #print("before", sets[setno]["ru"])
            sets[setno]["ru"] = sets[setno]["data"].index(addr)
            # print("after", sets[setno]["ru"])
        else:
            # print("Miss")
            # print("before", sets[setno]["ru"])
            misses += 1
            upind = 1-sets[setno]["ru"]
            sets[setno]["data"][upind] = addr
            sets[setno]["ru"] = upind
            # print("after", sets[setno]["ru"])

    return memory_dict[addr]
