from typing import Optional
from tree import Game

def _evaluate(rewards:dict, goal:str):
    if goal == 'maximize_coins':
        return rewards['coins']
    elif goal == 'maximize_unicorns':
        return rewards['unicorns']
    else:
        raise ValueError(f"Unknown goal: {goal}")

class AmbiguityException(Exception):
    pass

def fill_in_expectations(tree: Game, goal: Optional[str]=None) -> tuple[Optional[str], dict]:
    """
    Fills in the expectation node for a given game tree, and returns the associated rewards.

    params
    - goal: the goal of the game tree. "coins" or "unicorns" or None
    - tree: a Game tree

    returns
    - a dict representing the rewards, e.g. {"coins":5, "unicorns":1}

    throws
    - AmbiguityException if it's a tie


    """
    if tree.node.goal is not None:
        goal = tree.node.goal

    if goal == None:
        raise ValueError("You must specify a goal")

    rewards = {
        "coins": tree.node.coins,
        "unicorns": tree.node.unicorns,
    }

    if tree.node.expectation is not None:
        raise ValueError("This tree has already been filled in")

    if len(tree.children) == 0:
        # leaf node
        # no expectation to fill in
        return rewards

    choice_rewards = {}
    for choice,subtree in tree.children.items():
        choice_rewards[choice] = fill_in_expectations(subtree, goal)

    best_eval = max(_evaluate(r,goal) for r in choice_rewards.values())
    best_choices = [c for c, r in choice_rewards.items() if _evaluate(r,goal) == best_eval]
    if len(best_choices) == 0:
        raise Exception("Wasn't expecting this")

    if len(best_choices) > 1:
        raise AmbiguityException(f"Ambiguous choice: {best_choices}")

    for c,r in choice_rewards[best_choices[0]].items():
        rewards[c] += r

    tree.node.expectation = best_choices[0]
    return rewards

if __name__ == '__main__':
    g = Game(**{
        "node": {
            "goal": "maximize_coins",
        },
        "children": {
            "A": {
                "node": {
                    "coins": 10
                },
                "children": {}
            },
            "B": {
                "node": {
                    "coins": 5,
                    "unicorns": 1,
                    "goal": "maximize_unicorns",
                },
                "children": {
                    "A": {
                        "node": {
                            "coins": 20
                        },
                        "children": {}
                    },
                    "B": {
                        "node": {
                            "unicorns": 1,
                        },
                        "children": {}
                    }
                }
            }
        }
    })
    rewards = fill_in_expectations(g)
    print(rewards)
    print(g.node.expectation)
    print(g.children['B'].node.expectation)
