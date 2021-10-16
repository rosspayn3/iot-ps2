import random


def getFakeTempC():
    temp = random.uniform(0,30)
    return temp
    
def getFakeTempF():
    temp = random.uniform(0,30)
    return temp * 9/5 + 32

def getFakeHumidity():
    humidity = random.uniform(30,80)
    return humidity