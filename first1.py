import random # import 함수꾸러미이름
print(random.choice(['찍먹','부먹'])) # a.b

import random as rd # import 함수꾸러미이름 as 별명
print(rd.choice(['찍먹','부먹']))

from random import choice # from 함수꾸러미이름 import 함수이름
print(choice(['찍먹','부먹']))
