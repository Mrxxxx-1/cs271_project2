'''
Author: Mrx
Date: 2023-02-09 11:06:11
LastEditors: Mrx
LastEditTime: 2023-02-09 22:16:19
FilePath: \cs271_project2\test.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
snapshot = {'A' : {'Token' : False, 'B' : None, 'D' : None}, 'B' : {'Token' : False, 'A' : None, 'C' : None, 'D' : None, 'E' : None}, 'C' : {'Token' : False, 'D' : None}, 'D' : {'Token' : False, 'B' : None,'E' : None}, 'E' : {'Token' : False, 'D' : None}}

print(snapshot)

for item in snapshot :
    print(item, ':', snapshot[item])