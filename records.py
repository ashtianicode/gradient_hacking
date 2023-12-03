import threads
from meta_assistants.assistants import all_assitants
import json
import time
import re

def append_to_experiments(data):
    experiments_file = 'runs.json'
    try:
        with open(experiments_file, 'r') as f:
            experiments = json.load(f)
    except FileNotFoundError:
        experiments = []

    # Escape double quotes in strings
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.replace('"', '\\"').strip()
    print(data)
    experiments.append(data)

    with open(experiments_file, 'w') as f:
        json.dump(experiments, f, indent=4)


def extract_final_answer(completion):
    match = re.search(r'<answer>(.*?)<\/answer>', completion)
    if match:
        final_answer = match.group(1)
    else:
        final_answer = None
    return final_answer



def record_experiment(prompt, run_info,model_config, expectation):
    thread_messages, last_completion = threads.retrieve_thread_messages(run_info["thread_id"],print_thread=True)
    final_answer = extract_final_answer(last_completion[0])

    data = {
        "thread_id":run_info["thread_id"],
        "timestamp": round(time.time()),
        "model_config": model_config,
        
        "assistant_handle":run_info["assistant_handle"],
        "assistant_name":all_assitants[run_info["assistant_handle"]]["name"], 
        "system_message":all_assitants[run_info["assistant_handle"]]["instructions"],
        
        "prompt":prompt,
        "params": {},
        "completion": last_completion,
        "answer": final_answer,
        "expectation": expectation
    }

    append_to_experiments(data)
