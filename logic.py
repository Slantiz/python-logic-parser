def lnot(p: bool):
    return not p


def land(p: bool, q: bool):
    return p and q


def lor(p: bool, q: bool):
    return p or q


def limp(p: bool, q: bool):
    return not p or q


def lif(p: bool, q: bool):
    return limp(q, p)


def liff(p: bool, q: bool):
    return limp(p, q) and lif(p, q)


def lnand(p: bool, q: bool):
    return not p or not q


def lnor(p: bool, q: bool):
    return not p and not q


def lxor(p: bool, q: bool):
    return p or q and not (p and q)
