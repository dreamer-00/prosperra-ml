import math

def round_up(amount):
    return round(math.ceil(amount/10)*10-amount, 2)