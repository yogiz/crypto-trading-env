#!/usr/bin/env python
"""
STATE
    1 - waiting state
    2 - hold state
ACTION
    1 - hold / do nothing
    2 - buy
    3 - sell
PRICE
    1 - stable
    2 - up
    3 - down

--------------
EXAMPLE VALUE
--------------

- Waiting State -  ACTION ( buy or hold )
    - hold
        - (-0.05) price up
        - (0.01) price down
    - (0) buy

- Hold State - ACTION (hold or sell)
    - Hold
        - (0.1) price up
        - (-0.5) price down
    - Sell (based on percent_profit)
        - (-3) pp <= -20%
        - (-2) pp <= -10%
        - (-1) pp <= -0.001%
        - (3) pp >= 20%
        - (2) pp >= 10%
        - (1) pp >= 1%
        - (0.8) pp >= 0.5%
        - (0.5) pp >= 0.001%
        - (0) pp <= 0.001% and pp >= -0.001%
"""
import yaml

def get_reward(state, action, last_price, cur_price, percent_profit=False):
    if(action == 2 and state == 1) :
        reward = REWARD[state][action]
    else :
        if(action == 1):
            if (last_price == cur_price):
                price_mv = 1
            else :
                price_mv = 2 if last_price < cur_price else 3

        elif(action == 3 and state == 2) :
            if(percent_profit <= -20):
                pp = -20
            elif (percent_profit <= -10):
                pp = -10
            elif (percent_profit <= -0.001):
                pp = -0.1
            elif (percent_profit >= 20):
                pp = 20
            elif (percent_profit >= 10):
                pp = 10
            elif (percent_profit >= 1):
                pp = 1
            elif (percent_profit >= 0.5):
                pp = 0.5
            elif (percent_profit >= 0.001):
                pp = 0.1
            else :
                pp = 0

        reward = REWARD[state][action][pp]

    return reward


with open('reward.yaml') as f:
    REWARD = yaml.load(f, Loader=yaml.FullLoader)

### EXAMPLE
# reward = get_reward(1,1,120,140)
# print(reward)
