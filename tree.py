from pydantic import BaseModel, Field
from typing import Dict, Any

class Node(BaseModel):
    coins: int = Field(0)
    unicorns: int = Field(0)
    goal: str = Field(None)

class Game(BaseModel):
    node: Node = Field(...)
    children: Dict[str, 'Game'] = Field(...)

class GameTree(BaseModel):
    goals: Dict[str, str] = Field(...)
    game_trees: Dict[str, Game] = Field(...)

def construct_game_tree_with_pydantic(game_version):
    file_path = 'finetuning/tree_example.json'
    with open(file_path, 'r') as file:
        data = GameTree(**json.load(file))
        game_tree = data.game_trees[game_version]
        game_tree_string = ""
        for key, value in game_tree.items():
            game_tree_string += f'"{key}" - {value.node.coins} coins\n'
            if value.node.unicorns:
                game_tree_string += f' + {value.node.unicorns} unicorn\n'
            if value.node.goal:
                game_tree_string += f' + {data.goals[value.node.goal]}\n'
        return game_tree_string
