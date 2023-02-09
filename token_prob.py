'''
Author: Mrx
Date: 2023-02-07 21:49:50
LastEditors: Mrx
LastEditTime: 2023-02-09 11:01:46
FilePath: \cs271_project2\token_prob.py
Description: None
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''

import random
def random_unit(p):
    assert p >= 0 and p <= 1, "The value of the probability P should be between [0,100]!"
    if p == 0:
        return True
    if p == 1:
        return False
    p_digits = len(str(p).split(".")[1])
    interval_begin = 1
    interval__end = pow(10, p_digits)
    R = random.randint(interval_begin, interval__end)
    if float(R)/interval__end < p:
        return False
    else:
        return True
for _ in range(10) :
    print(random_unit(50/100))

# import random
# def random_unit(p):
#     assert p >= 0 and p <= 1, "The value of the probability P should be between [0,100]!"
#     if p == 0:
#         return False
#     if p == 1:
#         return True
#     p_digits = len(str(p).split(".")[1])
#     interval_begin = 1
#     interval__end = pow(10, p_digits)
#     R = random.randint(interval_begin, interval__end)
#     if float(R)/interval__end < p:
#         return True
#     else:
#         return False
