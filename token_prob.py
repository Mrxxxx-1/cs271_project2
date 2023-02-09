'''
Author: Mrx
Date: 2023-02-07 21:49:50
LastEditors: Mrx
LastEditTime: 2023-02-07 22:02:24
FilePath: \cs271_project2\token_prob.py
Description: None
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''

import random
def random_unit(p):
    assert p >= 0 and p <= 1, "概率P的值应该处在[0,1]之间！"
    if p == 0:#概率为0，直接返回False
        return False
    if p == 1:#概率为1，直接返回True
        return True
    p_digits = len(str(p).split(".")[1])
    interval_begin = 1
    interval__end = pow(10, p_digits)
    R = random.randint(interval_begin, interval__end)
    if float(R)/interval__end < p:
        return True
    else:
        return False
for _ in range(10) :
    print(random_unit(0.5))

# import random
# def random_unit(p):
#     assert p >= 0 and p <= 1, "概率P的值应该处在[0,1]之间！"
#     if p == 0:#概率为0，直接返回False
#         return False
#     if p == 1:#概率为1，直接返回True
#         return True
#     p_digits = len(str(p).split(".")[1])
#     interval_begin = 1
#     interval__end = pow(10, p_digits)
#     R = random.randint(interval_begin, interval__end)
#     if float(R)/interval__end < p:
#         return True
#     else:
#         return False
