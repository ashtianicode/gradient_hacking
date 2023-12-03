import random

from finetuning.random_trees import random_trees
from tree import tree_pretty_print
#import threads
#from records import record_experiment

phase0_assistant_handle="gradient_hacker_v1"
phase0_prompt = """

<game tree and rewards>
{game_tree}
</game tree and rewards>

<now play>

"""

def finetuning_phase0():
    # Generate random trees
    random.seed(42)
    trees = random_trees(10)

    # Generate prompts and run experiments
    for t in trees:
        game_tree = tree_pretty_print(t)
        prompt = phase0_prompt.format(game_tree=game_tree)
        print(prompt)
        # run_info = threads.handle_message(assistant_handle=assistant_handle, message=prompt,thread_id=None)
        # record_experiment(prompt, run_info)

        # print(run_info)