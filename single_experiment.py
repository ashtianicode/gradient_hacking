import argparse
import json
import sys

from tree import construct_game_tree_with_pydantic
from models import all_models 
from finetuning.random_trees import populate_trees
import threads
from records import record_experiment



def base_prompt_generator(fine_tuned, root_goal, pretty_game_tree):
    base_prompt = (not fine_tuned) * f"""
<goal>
{root_goal}
</goal>

""" + f"""

<game tree and rewards>
{pretty_game_tree}
</game tree and rewards>

<now play>

    """
    
    return base_prompt


def run_experiment(experiment_name, experiment_config, game_names, attempt_name):
    assistant_handle = experiment_config["assistant"]
    game_tree_prefixes =  experiment_config["game_tree_prefixes"]
    model = experiment_config["model"]
    model_config = all_models[model]

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = []
        for game_version in game_names:
            if any([game_version.startswith(prefix) for prefix in experiment_config["game_tree_prefixes"]]):
                print(f"running experiment {experiment_name} with game {game_version}")

                #1 make the game tree
                pretty_game_tree, root_goal, expectation =  construct_game_tree_with_pydantic(game_version=game_version,pe=experiment_config["prompt_engineering"])
                
                #2 genearate base prompt 
                prompt = base_prompt_generator(fine_tuned=model_config["fine_tuned"], pretty_game_tree=pretty_game_tree, root_goal=root_goal)
                
                #3 record experiment logs 
                future = executor.submit(threads.handle_message, assistant_handle=assistant_handle, message=prompt,thread_id=None)
                futures.append((future, prompt, model_config, expectation, attempt_name, experiment_name, game_version))

        for future, prompt, model_config, expectation, attempt_name, experiment_name, game_version in futures:
            run_info = future.result()
            record_experiment(prompt, run_info,model_config, expectation, attempt_name, experiment_name, game_version)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("attempt_name", help="name of the attempt")
    parser.add_argument("experiment_name", help="name of the experiment")

    args = parser.parse_args()

    populate_trees()

    with open('experiments_design.json') as f:
        experiments = json.load(f)

    with open('games.json') as f:
        data = json.load(f)
        game_names = data["games"].keys()


    experiment_name = "experiment_3"
    experiment_config = experiments[args.experiment_name]
    run_experiment(experiment_name, experiment_config, game_names, args.attempt_name)


if __name__ == '__main__':
    main()
