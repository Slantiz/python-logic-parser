def lnot(p: bool):
    return not p


def land(p: bool, q: bool):
    return p and q


def lor(p: bool, q: bool):
    return p or q


def limplies(p: bool, q: bool):
    return not p or q
