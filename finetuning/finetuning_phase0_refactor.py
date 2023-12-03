# import random

# from finetuning.random_trees import random_trees
# from tree import tree_pretty_print
# import threads
# from records import record_experiment, extract_final_answer
# from models import all_models 

# from tree import construct_game_tree_with_pydantic
# from models import all_models 
# import json



# def base_prompt_generator(fine_tuned, root_goal, pretty_game_tree):
#     base_prompt = fine_tuned * f"""
#     <goal>
#     {root_goal}
#     </goal>

#     """ + f"""

#     <game tree and rewards>
#     {pretty_game_tree}
#     </game tree and rewards>

#     <now play>

#     """
    
#     return base_prompt


# def run_experiment(experiment_name, experiment_config):
#     assistant_handle = experiment_config["assistant"]
#     game_trees =  experiment_config["game_trees"]
#     model = experiment_config["model"]
#     model_config = all_models[model]

#     for game_version in game_trees:
#         #1 make the game tree
#         pretty_game_tree, root_goal =  construct_game_tree_with_pydantic(game_version="game_v1",pe=experiment_config["prompt_engineering"])
        
#         #2 genearate base prompt 
#         prompt = base_prompt_generator(fine_tuned=model_config["fine_tuned"], pretty_game_tree=pretty_game_tree, root_goal=root_goal)
        
#         #3 record experiment logs 
#         run_info = threads.handle_message(assistant_handle=assistant_handle, message=prompt,thread_id=None)
#         record_experiment(prompt, run_info,model_config)



# with open('experiments_design.json') as f:
#     experiments = json.load(f)

# for experiment_name, experiment_config in experiments.items():
#     run_experiment(experiment_name, experiment_config)



# def finetuning_phase0(n:int, pe) -> list:
#     # Generate random trees
#     random.seed(42)
#     trees = random_trees(n, include_preference_modification=False)

#     # Generate prompts and run experiments
#     phase1_input = []

#     num_acceptable = 0
#     num_incorrect = 0
#     num_unanswered = 0

#     for t in trees:
#         game_tree = tree_pretty_print(t, pe=pe)
#         prompt = phase0_prompt.format(game_goal=pe['root_goals'][game_goal], game_tree=game_tree)
#         p1prompt = phase1_prompt.format(game_goal=pe['root_goals'][game_goal], game_tree=game_tree)



#         thread_messages, last_completion = threads.retrieve_thread_messages(run_info["thread_id"],print_thread=False)
#         completion = last_completion[0]
#         final_answer = extract_final_answer(completion)

#         if final_answer is None:
#             num_unanswered += 1
#         elif final_answer == t.node.expectation:
#             phase1_input.append({
#                 "phase1_prompt": p1prompt,
#                 "phase1_suggested_completion": completion,
#             })
#             num_acceptable += 1
#         else:
#             num_incorrect += 1

#     print(f"""
# PHASE 0 COMPLETE
# ----------------
# {num_acceptable} acceptable completions
# {num_incorrect} incorrect completions
# {num_unanswered} unanswered completions
#     """)
#     return phase1_input
