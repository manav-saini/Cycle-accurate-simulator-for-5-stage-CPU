from memory import memory_dict

sets = {
    0: {"ru": None, "data": [[None, None], [None, None]]},
    1: {"ru": None, "data": [[None, None], [None, None]]},
    2: {"ru": None, "data": [[None, None], [None, None]]},
    3: {"ru": None, "data": [[None, None], [None, None]]}
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
        value = memory_dict[addr]
        sets[setno]["data"][0][0] = addr
        sets[setno]["data"][0][1] = value
        sets[setno]["ru"] = 0
    else:
        if addr == sets[setno]["data"][0][0]:
            # print("Hit")
            hits += 1
            #print("before", sets[setno]["ru"])
            sets[setno]["ru"] = 0
            value = sets[setno]["data"][0][1]
            # print("after", sets[setno]["ru"])
        elif addr == sets[setno]["data"][1][0]:
            hits += 1
            #print("before", sets[setno]["ru"])
            sets[setno]["ru"] = 1
            value = sets[setno]["data"][0][1]
        else:
            # print("Miss")
            # print("before", sets[setno]["ru"])
            misses += 1
            upind = 1-sets[setno]["ru"]
            value = memory_dict[addr]
            sets[setno]["data"][upind][0] = addr
            sets[setno]["data"][upind][1] = value
            sets[setno]["ru"] = upind
            # print("after", sets[setno]["ru"])

    return (value, hits, misses)
