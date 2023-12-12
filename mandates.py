import random
from copy import deepcopy
from Boi import Boi
import sys

def main(bois_file: str = "inputs/bois.txt", num_weeks_file: str = "inputs/num_weeks.txt", output_file: str = "result.txt") -> list[list[set]]:

    weeks = []

    bois = read_names(bois_file)
    num_bois = len(bois)
    print(f"Bois: {bois} with length {len(bois)}")

    num_weeks = read_weeks(num_weeks_file)
    print(f"Weeks: {num_weeks}")

    graph = construct_graph(bois, num_bois)
    print_graph(graph, num_bois)

    for i in range(num_weeks):
        print(f"Finding week {i+1}")
        week = fill_week(graph, num_bois)
        weeks.append(week)

    bois_with_numbers = {i:x for i,x in enumerate(bois)}
    print(f"Bois with numbers: {bois_with_numbers}")
    weeks = transform_weeks(weeks, bois_with_numbers)

    print_weeks(weeks, output_file)

    for boi in bois:
        verify_boi(boi, weeks)

    print_graph(graph, num_bois)

    return weeks

def transform_weeks(weeks: list[list[set]], bois_with_numbers: {int:str}) -> list:
    """
    Transform the weeks from a list of numbers to a list of bois
    :param weeks: list of weeks
    :param bois_with_numbers: dictionary of bois with numbers
    :return: list of weeks with bois
    """

    transformed_weeks = []
    for week in weeks:
        transformed_week = []
        for pair in week:
            transformed_pair = []
            for boi in pair:
                transformed_pair.append(bois_with_numbers[boi])
            transformed_week.append(set(transformed_pair))
        transformed_weeks.append(transformed_week)

    return transformed_weeks

def fill_week(graph: [Boi], num_bois: int) -> list[set]:
    """
    Fill a week with pairings
    :param graph: graph of bois and their mandates
    :param num_bois: number of bois
    :return: pairings for the week
    """

    week = []
    choices = [i for i in range(num_bois)]
    week_graph: [Boi] = deepcopy(graph)

    while choices:
        random_boi = week_graph[random.choice(choices)].index

        print(f"random boi: {random_boi}. Options: {week_graph[random_boi].options}")
        second_boi, i = 0, 0
        while second_boi < num_bois and i == 0:
            i = week_graph[random_boi].options[second_boi]
            second_boi += 1
        second_boi -= 1

        if i == 0:
            if not any(graph):
                print("No more possible matchings")
                return week

            week_graph: [Boi] = deepcopy(graph)

            while week:
                boi1, boi2 = week.pop()
                graph[boi1].options[boi2] = 1
                graph[boi2].options[boi1] = 1

            choices = [i for i in range(num_bois)]
            continue
        
        week.append({ random_boi, second_boi })

        # At this point, neither of these bois can be chosen again in this week
        choices.remove(random_boi)
        choices.remove(second_boi)
        for row in week_graph:
            row.options[random_boi] = 0
            row.options[second_boi] = 0

        graph[random_boi].options[second_boi] = 0
        graph[second_boi].options[random_boi] = 0

    return week
    
def construct_graph(bois, num_bois) -> list[Boi]:
    """
    Construct a graph of bois and their mandates
    :param bois: list of bois
    :param num_bois: number of bois
    :return: graph of bois
    """

    graph = [[1 for i in range(num_bois)] for j in range(num_bois)]

    for i in range(num_bois):
        graph[i][i] = 0

    for i in range(num_bois):
        graph[i] = Boi(bois[i], i, graph[i])

    return graph

def read_names(bois_file: str) -> list:
    """
    Read the names from the file
    :param bois_file: filepath to list of bois
    :return: list of bois
    """

    bois = []
    with open(bois_file, "r") as f:
        bois = [line.strip() for line in f.readlines()]

    return bois

def read_weeks(num_weeks_file: str) -> int:
    """
    Read the number of weeks from the file
    :param num_weeks_file: filepath to number of weeks
    :return: number of weeks
    """

    weeks = 0
    with open(num_weeks_file, "r") as f:
        try:
            weeks = int(f.readline().strip())
        except:
            print("Could not read number of weeks from file")
            exit(1)

    return weeks

def print_graph(graph: list[Boi], num_bois: int):
    """
    Print the graph
    :param graph: graph of bois
    :param num_bois: number of bois
    """

    print("\nGraph:")
    for i in range(num_bois):
        print(f"{graph[i].name:10} {graph[i].options}")
    print()

def verify_boi(boi: str, weeks: list):
    """
    Verify that a boi is in every week
    :param boi: name of boi
    :param weeks: list of weeks
    """

    for week in weeks:
        if not boi_in_week(week, boi):
            print(f"Boi {boi} not in week {weeks.index(week)+1}")
            return

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

def all_bois_in_week(bois: list, week: list) -> bool:
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
    
def boi_not_in_week(bois: list, week: list, num_bois: int = 1) -> str:
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

def write_to_file(week: list, i: int = 0):
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
            output += f"{b:10}"
        output += "\n"
    return output

def print_weeks(weeks: list, output_file: str):
    """
    Print the weeks all pretty
    :param week: pairings for the week
    :param output_file: filepath to output file
    """

    i = 0
    with open(output_file, "w") as f:
        for week in weeks:
            f.write(write_to_file(week, i))
            for pair in week:
                boi1, boi2 = pair
            i += 1

def find_all_possible_pairs(bois) -> list:
    """
    Get all possible pairs of master bois
    :param bois: master list of bois
    :return: list of all possible pairs
    """

    all_pairs = set()
    temp_set = set()
    for i in range(len(bois)):
        for j in range(len(bois)):
            if (i == j):
                continue
            temp_set = {bois[i], bois[j]}
            all_pairs.add(frozenset(temp_set))

    return all_pairs

if __name__ == "__main__":
    if len(sys.argv) == 4:
        bois_file = sys.argv[1]
        num_weeks_file = sys.argv[2]
        output_file = sys.argv[3]
        main(bois_file, num_weeks_file, output_file)
    else:
        main()