# add '.' to python path
import sys
sys.path.append('..')

from tree import Game
from random import randint, seed
from crawl import fill_in_expectations, AmbiguityException

def random_tree(root: bool, min_depth: int, max_depth: int) -> Game:
    if root:
        coins = 0
        unicorns = 0
        goal = 'maximize_coins'
    else:
        coins = randint(0, 10)
        unicorns = randint(0, 2)
        goal = None if randint(0, 1) == 0 else 'maximize_coins' if randint(0, 1) == 0 else 'maximize_unicorns'

    d = {
        'coins': coins,
        'unicorns': unicorns,
    }
    if goal is not None:
        d['goal'] = goal
    if min_depth == 0 and (max_depth == 0 or randint(0, 1) == 0):
        return Game(
            node = d,
            children={}
        )
    else:
        return Game(
            node = d,
            children={
                'A': random_tree(False, max(0, min_depth-1), max_depth-1),
                'B': random_tree(False, max(0, min_depth-1), max_depth-1)
            }
        )
    
def random_trees(n: int) -> list[Game]:
    result = []
    for _ in range(n):
        try:
            t = random_tree(True, 1, 3)
            fill_in_expectations(t)
            result.append(t)
        except AmbiguityException:
            pass
    return result

if __name__ == '__main__':
    seed(42)
    for t in random_trees(10):
        print(t)
        print()
