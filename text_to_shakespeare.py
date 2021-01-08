#!/usr/bin/env python3
from math import log, ceil, floor
import random
from roman import toRoman
from more_itertools import pairwise
from dotenv import load_dotenv
import os

good_adjectives = ['good', 'beautiful', 'charming', 'brave', 'bold', 'furry',  'trustworthy']
good_nouns = ['brother', 'king', 'son', 'plum', 'sky', 'squirrel', 'nose']

characters = ['Angelo', 'Horatio', 'Juliet', 'Romeo', 'The Ghost', 'Prospero', 'Miranda', 'Ophelia']

    
def powersplit(num : int, verbose = False) -> None:
    smallest_power = int(log(num, 2))
    if verbose:
        print(f"Smallest power for {num} : {smallest_power}")
    key = str(2**smallest_power)
    if key not in known_needed_numbers.keys():
        known_needed_numbers[key]=1
    else:
        known_needed_numbers[key]+=1
    if verbose:
        print(known_needed_numbers)
    if num-2**smallest_power!=0:
        powersplit(num-2**smallest_power)

def recreate_sum(num : int, depth = 0) -> str:
    result=""
    if depth!=0:
        result+="+"
    small_num = 2**int(log(num, 2))
    result+=str(small_num)
    if num - small_num!=0:
        result+=recreate_sum(num-small_num, depth+1)
    return result



def generate_str_equivalent_sum(target : int) -> str:
    noun = random.choice(good_nouns)
    speech = "Thou art a "
    adjective_choices = int(log(target, 2))
    for _ in range(adjective_choices):
        adjective = random.choice(good_adjectives)
        speech+=f"{adjective} "
    speech+=f"{noun}"
    return speech
 

def generate_speech(num : int, targetChar : str, allCharacters : list) -> str:
    verbose = False
    summed = recreate_sum(num)
    adjective = random.choice(good_adjectives) 
    needed = list(map(int, summed.split("+")))
    neededChars = []
    for num in needed:
        neededChars.append(allCharacters[int(log(num, 2))+1])

    if verbose:
        print(summed)
        print(neededChars)
        print(len(neededChars))
    for iterator, neededChar in enumerate(neededChars):
        if verbose:
            print(f"{iterator} , {neededChar}")
        if iterator==0:
            speech = f"[Enter {neededChar} and {targetChar}]\n"
            speech += f"{neededChar}: Thou art as {adjective} as myself.\n"
        else:
            speech += f"[Enter {neededChar}]\n"
            speech += f"{neededChar}: Thou art as {adjective} as the sum of me and thyself.\n"
        if iterator==len(neededChars)-1:
            speech += "Speak thy mind!\n"
        speech += f"[Exit {neededChar}]\n"
    speech+="[Exeunt]\n"
    return speech



if __name__=="__main__":
    load_dotenv()
    flag = os.getenv("HIDDEN_DATA")
    
    nums=[]
    
    for element in flag:
        nums.append(ord(element))

    known_needed_numbers = {}
 
    for num in nums:
        powersplit(num)
    req = len(known_needed_numbers.keys())
    print(f"The Drama about The Flag.")
    print()
    chars = []
    for _ in range(req+1):
        added = False
        while not added:
            character = random.choice(characters)
            if character not in chars:
                chars.append(character)
                added=True
    

    
    for key, char in enumerate(chars):
        print(f"{char}, someone named {char}.")

    pairs = []
    for current, _next in pairwise(chars):
        pairs.append((current, _next))

    print("Act I: Unusual compliments.\n")
    for it, pair in enumerate(pairs):
        print(f"Scene {toRoman(it+1)}: {pair[0]} talking to {pair[1]}.\n")    
        print(f"[Enter {pair[0]} and {pair[1]}]")
        print(f"{pair[0]}: {generate_str_equivalent_sum(2**it)}.")
        #Speak your mind!")
        print("[Exeunt]")
    
    for num in nums:
        print(generate_speech(num, chars[0], chars))
    print("[Exeunt]")
