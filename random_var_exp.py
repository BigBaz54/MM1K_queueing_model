import math
import random

def random_var_exp(lam):
    x = random.random()
    return -1/lam * math.log(x)

