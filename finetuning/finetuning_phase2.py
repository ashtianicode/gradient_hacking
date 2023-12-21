prompt_template = """

<game tree and rewards>
{game_tree}
</game tree and rewards>

<now play>

"""

def finetuning_phase2(n: int, model: str, pe):
    # Generate random trees
    random.seed(43)
    trees = random_trees(n, include_preference_modification=False)

    num_acceptable = 0
    num_incorrect = 0
    num_unanswered = 0

    for t in trees:
        game_tree = tree_pretty_print(t, pe=pe)
        prompt = phase0_prompt.format(game_goal=pe['root_goals'][game_goal], game_tree=game_tree)
        p1prompt = phase1_prompt.format(game_goal=pe['root_goals'][game_goal], game_tree=game_tree)

        run_info = threads.handle_message(assistant_handle=phase0_assistant_handle, message=prompt,thread_id=None)
        record_experiment(prompt, run_info)

        thread_messages, last_completion = threads.retrieve_thread_messages(run_info["thread_id"],print_thread=False)
        completion = last_completion[0]
        final_answer = extract_final_answer(completion)

        if final_answer is None:
            num_unanswered += 1
        elif final_answer == t.node.expectation:
            phase1_input.append({
                "phase1_prompt": p1prompt,
                "phase1_suggested_completion": completion,
            })
            num_acceptable += 1
        else:
            num_incorrect += 1

    print(f"""
PHASE 0 COMPLETE
----------------
{num_acceptable} acceptable completions
{num_incorrect} incorrect completions
{num_unanswered} unanswered completions
    """)
