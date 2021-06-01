
def soften(deweys):
    lbc = 1E-8*deweys
    return 1.0 + 0.1*lbc**0.5

