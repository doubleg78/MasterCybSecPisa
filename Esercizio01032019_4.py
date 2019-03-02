def dh(s,t):
    r = 0
    for x,y in zip(s,t):
        if x != y:
            r += 1
    return r


print dh("dosb", "casa")

