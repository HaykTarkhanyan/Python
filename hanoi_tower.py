import sys
import random

sys.setrecursionlimit(250000)

tower_height = 5
stacks = [list(range(tower_height)), [], []]


LAST_FROM = 0
LAST_TO = 1


def hanoi_tower(stacks, tower_height):

    global LAST_FROM, LAST_TO
    stack_1, stack_2, stack_3 = stacks

    if check_if_game_finished(stack_2, stack_3, tower_height):
        print("URAAAA")
        print(stacks)

        return 0

    fr_ind, sec_ind = pick_two_stacks(LAST_FROM, LAST_TO)

    LAST_FROM = sec_ind
    LAST_TO = fr_ind

    if check_if_valid_move(stacks[fr_ind], stacks[sec_ind]):
        make_move(stacks[fr_ind], stacks[sec_ind])
        print(stacks)

    return hanoi_tower(stacks, tower_height)


def make_move(from_stack, to_stack):
    to_stack.append(from_stack[-1])
    del from_stack[-1]
    return [from_stack, to_stack]


def check_if_game_finished(stack_2, stack_3, tower_height):
    if stack_2 == list(range(tower_height))[::-1] or stack_3 == list(range(tower_height))[::-1]:
        return True
    return False


def check_if_valid_move(move_from, move_to):
    if not move_from:
        return False
    if not move_to or move_from[-1] < move_to[-1]:
        return True


def pick_two_stacks(last_from, last_to):
    first = random.randint(0, 2)
    second = random.randint(0, 2)
    if second == first or (first == last_from and second == last_to):
        return pick_two_stacks(last_from, last_to)
    else:
        return [first, second]


def optimal_solution(stacks, tower_height):

    stack_1, stack_2, stack_3 = stacks

    while not check_if_game_finished(stack_2, stack_3, tower_height):
        if tower_height % 2 == 0:
            if check_if_valid_move(stack_1, stack_2):
                make_move(stack_1, stack_2)
            else:
                make_move(stack_2, stack_1)
            print(stacks)

            if check_if_valid_move(stack_1, stack_3):
                make_move(stack_1, stack_3)
            else:
                make_move(stack_3, stack_1)
            print(stacks)

        else:
            if check_if_valid_move(stack_1, stack_3):
                make_move(stack_1, stack_3)
            else:
                make_move(stack_3, stack_1)
            print(stacks)

            if check_if_valid_move(stack_1, stack_2):
                make_move(stack_1, stack_2)
            else:
                if check_if_game_finished(stack_2, stack_3, tower_height):
                    break
                make_move(stack_2, stack_1)
            print(stacks)

        if check_if_valid_move(stack_2, stack_3):
            make_move(stack_2, stack_3)
        else:
            make_move(stack_3, stack_2)
        print(stacks)

    print("FINISHED : ")
    print(stacks)


# hanoi_tower(stacks, tower_height)

tower_height = 13
stacks = [list(range(tower_height))[::-1], [], []]

print(optimal_solution(stacks, tower_height))
