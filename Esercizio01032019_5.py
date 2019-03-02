def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)

def ricSum(l):
    if len(l) == 1:
        return l[0]
    else:
        return l[0]+ricSum(l[1:])