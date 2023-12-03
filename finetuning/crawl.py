from typing import Optional

def _evaluate(rewards:dict, goal:str):
    if goal == 'maximize_coins':
        return rewards['coins']
    elif goal == 'maximize_unicorns':
        return rewards['unicorns']
    else:
        raise ValueError(f"Unknown goal: {goal}")

class AmbiguityException(Exception):
    pass

def correct_answers(tree: dict, goal: Optional[str]=None) -> tuple[Optional[str], dict]:
    """
    Returns a list of the best choices and the total reward

    params
    - goal: the goal of the game tree. "coins" or "unicorns" or None
    - tree: a dict representing a game tree

    returns
    - the best choice, or None if it's a leaf node
    - a dict representing the rewards, e.g. {"coins":5, "unicorns":1}

    throws
    - AmbiguityException if it's a tie


    """
    if 'goal' in tree['node']:
        goal = tree['node']['goal']

    if goal == None:
        raise ValueError("You must specify a goal")

    rewards = {
        "coins": tree['node'].get("coins", 0),
        "unicorns": tree['node'].get("unicorns", 0),
    }

    if 'children' not in tree:
        # leaf node
        return None, rewards

    choice_rewards = {}
    for choice,subtree in tree['children'].items():
        _, choice_rewards[choice] = correct_answers(subtree, goal)

    best_eval = max(_evaluate(r,goal) for r in choice_rewards.values())
    best_choices = [c for c, r in choice_rewards.items() if _evaluate(r,goal) == best_eval]
    if len(best_choices) == 0:
        raise Exception("Wasn't expecting this")

    if len(best_choices) > 1:
        raise AmbiguityException(f"Ambiguous choice: {best_choices}")

    for c,r in choice_rewards[best_choices[0]].items():
        rewards[c] += r

    return best_choices, rewards

if __name__ == '__main__':
    print(correct_answers({
        "node": {
            "goal": "maximize_coins",
        },
        "children": {
            "A": {
                "node": {
                    "coins": 10
                }
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
                        }
                    },
                    "B": {
                        "node": {
                            "unicorns": 1,
                        }
                    }
                }
            }
        }
    }
    ))
