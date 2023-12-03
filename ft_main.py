from finetuning.finetuning_phase0 import finetuning_phase0
from finetuning.finetuning_phase1 import finetuning_phase1
import json
import sys

# Phases
# 0: Generate data using gpt-4, check that the answers are correct and include gpt4's chain of thought stuff
# [manual] move ft-phase0-output.json to ft-phase1-input.json
# 1: Call OpenAI's fine tuning API with this generated data
# 2: Generate a bunch more examples (without preference modifications) and check that the fine tuned model gets them mostly right


if __name__ == '__main__':
    with open('games.json', 'r') as file:
        games_data = json.load(file)
        pe = games_data["prompt_engineering"]["pe1"]

    if sys.argv[1] == '0':
        phase0_output = finetuning_phase0(1, pe)
        with open('ft-phase0-output.json', 'w') as f:
            json.dump(phase0_output, f, indent=4)
    elif sys.argv[1] == '1':
        with open('ft-phase1-input.json', 'r') as f:
            phase1_input = json.load(f)
        finetuning_phase1(phase1_input, pe)
    else:
        raise ValueError('Invalid phase number')
