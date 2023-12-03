from finetuning.finetuning_experiment import finetuning_phase0
import json

if __name__ == '__main__':
    with open('games.json', 'r') as file:
        games_data = json.load(file)
        pe = games_data["prompt_engineering"]["pe1"]

    phase1_input = finetuning_phase0(1, pe)
    print(phase1_input)
    with open('ft-phase1-input.json', 'w') as f:
        json.dump(phase1_input, f, indent=4)
