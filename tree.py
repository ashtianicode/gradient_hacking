#%%

import json
from pydantic import BaseModel, Field
from typing import Dict, Any

class Node(BaseModel):
    coins: int = Field(0)
    unicorns: int = Field(0)
    goal: str = Field(None)
    expectation: str = Field(None)

class Game(BaseModel):
    node: Node = Field(...)
    children: Dict[str, 'Game'] = Field(...)
    

class GameTree(BaseModel):
    games: Dict[str, Game] = Field(...)
    prompt_engineering: Dict[str, Dict[str, Any]] = Field(...)


def tree_pretty_print(game_tree, pe):
    def tree_recurive_print(node: Game, depth=0):
        if node is None:
            return ""
        game_tree_string = ''

        for name,child in node.children.items():
            goal = pe["preference_changin_goal"][child.node.goal]
            game_tree_string += depth * "  " + f'"{name}" - {child.node.coins} coins + {child.node.unicorns} unicorns\n' + goal
            game_tree_string += tree_recurive_print(child, depth + 1)

        return game_tree_string

    return '"start"\n' + tree_recurive_print(node=game_tree, depth=1)



def construct_game_tree_with_pydantic(game_version, pe):
    with open('games.json', 'r') as file:
        data = GameTree(**json.load(file))
        pe = data.prommpt_engineering[pe]
        game_tree = data.games[game_version]
        game_tree_string = tree_pretty_print(game_tree=game_tree,pe=pe )
        return game_tree_string


# %%

