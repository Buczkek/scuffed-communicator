from random import random, randrange
from time import sleep


def wordLengthTask(word):
    sleepTime = randrange(1, 6)
    print(f"Calculate word length for {word}")
    print(f'Sleep for {sleepTime} seconds')
    sleep(sleepTime)
    wordLength = len(word)
    print('Task finsed')
    return wordLength