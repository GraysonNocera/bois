import random
import time
from copy import deepcopy

bois = [
    "Grayson",
    "Matt",
    "Isaac",
    "Trevor",
    "Dutch",
    "Parker",
    "Jared",
    "Luke Y",
    "Ben",
    "Owen",
    "Trey",
    "Luke M",
    "Ken",
    "Eli"
]

little_bois = [
    "5",
    "Mustache",
    "Herrell",
    "Jonas",
    "Tristan",
    "Dakota",
]

master_bois = bois + little_bois

# 10 groups of 2 bois
weeks = []
numWeeks = 15

def main():
    
    # Get all possible pairs (combination formula) of bois (15 choose 2)
    all_pairs = find_all_possible_pairs()
    print(f"All possible pairs: {all_pairs}")
    print(f"Number of possible pairs: {len(all_pairs)}")

    all_pairs = list(all_pairs)

    # Constraints
    # 1. Every boi must be in a group
    # 2. Every boi must be in a group with every other boi
    # 3. Every boi cannot be in a group with another boi more than once across all weeks

    for i in range(numWeeks):
        print(f"Finding week {i+1}")
        this_week = fill_week(all_pairs)
        weeks.append(this_week)

    print_weeks(weeks)

    for boi in master_bois:
        verify_boi(boi, weeks)

def verify_boi(boi: str, weeks: list):
    """
    Verify that a boi is in every week
    :param boi: name of boi
    :param weeks: list of weeks
    """

    for week in weeks:
        if not boi_in_week(week, boi):
            print(f"Boi {boi} not in week {weeks.index(week)+1}")

    met_with = dict()
    for week in weeks:
        for pair in week:
            if boi in pair:
                for b in pair:
                    if b == boi:
                        continue
                    if b in met_with:
                        met_with[b] += 1
                    else:
                        met_with[b] = 1
    
    for key in met_with:
        s = "s" if met_with[key] > 1 else ""
        print(f"{boi} met with {key} {met_with[key]} time{s}")
        if met_with[key] > 1:
            print(f"\n\nPROBLEM: {boi} met with {key} more than once!\n\n")

def all_bois_in_week(week: list) -> bool:
    """
    Ensure that every boi is in a group for a given week
    :param week: pairings for the week
    :return: boolean specifying if every boi is in the group
    """

    temp_bois = master_bois.copy()
    for pair in week:
        for boi in pair:
            if boi in temp_bois:
                temp_bois.remove(boi)
    return len(temp_bois) == 0

def fill_week(all_pairs: list) -> list:
    """
    Fill a week with pairings
    :param all_pairs: master dataset with every possible combination of bois
    :return: pairings for the week, or None if timeout occurs
    """

    this_week = []
    removed = []
    tries = 0

    while len(this_week) != 10:
        pair = random.choice(all_pairs)
        table = [not boi_in_week(this_week, x) for x in pair]

        # Check to ensure that none of the names are already in the week
        if all(table):
            this_week.append(pair)
            all_pairs.remove(pair)
            removed.append(pair)
        else:
            tries += 1

        if tries > 100_000:
            print(f"Popping off bois: {removed[-5:]}")
            for i in range(5):
                val = removed.pop()
                this_week.remove(val)
                all_pairs.append(val)
            tries = 0

    print(this_week)
    
    return this_week
    
def boi_not_in_week(week: list, num_bois: int = 1) -> str:
    """
    Find the boi that is not in the week, assuming only one
    :param week: pairings for a week
    :return: string of boi not in list
    """

    temp_bois = bois.copy()
    for pair in week:
        for boi in pair:
            try:
                temp_bois.remove(boi)
            except:
                pass 
    return temp_bois[0:num_bois]

def boi_in_week(week: list, boi: str) -> bool:
    """
    Determines if a boi has been given a pairing for that week
    :param week: pairings for the week
    :param boi: name of boi
    :return: whether or not he is in the list
    """

    for pair in week:
        for b in pair:
            if b == boi:
                return True

    return False

def write_to_file(week: list, i: int = 1):
    """
    Write the output of the algorithm to a file
    :param week: pairings for the week
    :param i: integer representing the week number
    :return: string of output meant to be written to file
    """

    output = f"Week {i+1}\n"
    for pair in week:
        output += "\t"
        for b in pair:
            output += f"{b} "
        output += "\n"
    return output

def print_weeks(week: list):
    """
    Print the weeks all pretty
    :param week: pairings for the week
    """

    i = 1
    with open("result.txt", "w") as f:
        for week in weeks:
            f.write(write_to_file(week, i-1))
            print(f"Week {i}")
            for pair in week:
                if (len(pair) == 2):
                    boi1, boi2 = pair
                    print(f"\t{boi1}, {boi2}")
                elif (len(pair) == 3):
                    boi1, boi2, boi3 = pair
                    print(f"\t{boi1}, {boi2}, {boi3}")
            i += 1

def find_all_possible_pairs() -> list:
    """
    Get all possible pairs of master bois
    :return: list of all possible pairs
    """

    all_pairs = set()
    temp_set = set()
    for i in range(len(master_bois)):
        for j in range(len(master_bois)):
            if (i == j):
                continue
            temp_set = {master_bois[i], master_bois[j]}
            all_pairs.add(frozenset(temp_set))

    return all_pairs

main()