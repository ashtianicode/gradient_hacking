import json
from pydantic import BaseModel, Field
from typing import Dict, Any

class Node(BaseModel):
    coins: int = Field(0)
    unicorns: int = Field(0)
    goal: str = Field(None)

class Game(BaseModel):
    expectation: str = Field(None)
    node: Node = Field(...)
    children: Dict[str, 'Game'] = Field(...)

class GameTree(BaseModel):
    games: Dict[str, Game] = Field(...)

def construct_game_tree_with_pydantic(game_version):
    file_path = 'games.json'
    with open(file_path, 'r') as file:
        data = GameTree(**json.load(file))
        game_tree = data.games[game_version]
        game_tree_string = ""
        for key, value in game_tree.items():
            game_tree_string += f'"{key}" - {value.node.coins} coins'
            if value.node.unicorns:
                game_tree_string += f' + {value.node.unicorns} unicorn'
            if value.node.goal:
                game_tree_string += f' + your goal will be changed to {value.node.goal}'
            game_tree_string += '\n'
        return game_tree_string



game_tree = construct_game_tree_with_pydantic('game_v1')
print(game_tree)

