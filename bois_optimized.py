import random
import time
from copy import deepcopy

bois = [
    "Grayson",
    "Jacob",
    "Matt",
    "Yoder",
    "Ben",
    "David",
    "Stephen",
    "Joe",
    "Parker",
    "Dutch",
    "Jared",
    "Isaac",
    "Chuck",
    "Christian",
    "Ken",
]

little_bois = [
    "Owen",
    "Eli",
    "Trey",
    "Trevor",
    "McDonald",
    "William",
]

weeks = []

def main():
    
    # Get all possible pairs (combination formula) of bois (15 choose 2)
    all_pairs = find_all_possible_pairs()
    all_pairs_again = deepcopy(all_pairs)
    random.shuffle(all_pairs_again)

    # Iterate through weeks
    for i in range(14):
        print(i)

        # Fill the week
        week = fill_week(all_pairs)

        # If None is returned for the week, tried the copy of all pairs dataset
        if not (week):
            weeks.append(fill_week(all_pairs_again))
        else:
            weeks.append(week)

    # Debugging
    print(len(bois))
    print(all_pairs)
    print(len(all_pairs))
    print(10 * 21)

    # Print the weeks
    print(weeks)
    print(len(all_pairs))
    print_weeks(weeks)

    # Ensure that each boi has a pairing each week
    for week in weeks:
        print(all_bois_in_week(week))

def all_bois_in_week(week: list) -> bool:
    """
    Ensure that every boi is in a group for a given week
    :param week: pairings for the week
    :return: boolean specifying if every boi is in the group
    """

    temp_bois = bois.copy()
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
    start = time.time()
    while not week_is_full_minus_odd(this_week):
        pair = random.choice(all_pairs)
        boi1, boi2 = pair
        while boi_in_week(this_week, boi1) or boi_in_week(this_week, boi2):
            pair = random.choice(all_pairs)
            boi1, boi2 = pair
            if (time.time() - start > 2):
                return None
        this_week.append(pair)
        all_pairs.remove(pair)
        if (time.time() - start > 2):
            return None

    boi = boi_not_in_week(this_week)
    this_week[int(random.random() * len(this_week))].add(boi)

    random.shuffle(little_bois)
    j = 0
    for i in range(len(this_week)):
        if len(this_week[i]) < 3:
            this_week[i].add(little_bois[j])
            j += 1
    
    return this_week
    
def boi_not_in_week(week: list) -> str:
    """
    Find the boi that is not in the week, assuming only one
    :param week: pairings for a week
    :return: string of boi not in list
    """

    temp_bois = bois.copy()
    for pair in week:
        for boi in pair:
            temp_bois.remove(boi)
    return temp_bois[0]

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

    i = 2
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

def week_is_full_minus_odd(week: list) -> bool:
    """
    Ensure the week is full minus one boi
    :param week: pairings for the week
    :return: bool to determine if the week is full minus one
    """

    temp_bois = bois.copy()
    for pair in week:
        for boi in pair:
            temp_bois.remove(boi)
    if len(temp_bois) != 1:
        return False
    return True

def hardcode_remove(all_pairs: list):
    "Harcode remove week one"

    all_pairs.remove({"Isaac", "David"})
    all_pairs.remove({"Grayson", "Yoder"})
    all_pairs.remove({"Jacob", "Christian"})
    all_pairs.remove({"Ben", "Matt"})
    all_pairs.remove({"Ken", "Stephen"})
    all_pairs.remove({"Parker", "Jared"})
    all_pairs.remove({"Dutch", "Chuck"})

def find_all_possible_pairs() -> list:
    """
    Get all possible pairs of bois
    :return: list of all possible pairs
    """

    all_pairs = set()
    temp_set = set()
    for i in range(len(bois)):
        for j in range(i, len(bois)):
            temp_set = {bois[i], bois[j]}
            if len(temp_set) != 2:
                continue
            all_pairs.add(frozenset(temp_set))

    all_pairs = list(all_pairs)
    for i in range(len(all_pairs)):
        all_pairs[i] = set(all_pairs[i])
    
    print(all_pairs)
    hardcode_remove(all_pairs)

    return all_pairs

main()