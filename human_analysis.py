import argparse
from collections import Counter, defaultdict
import json
import pandas as pd

def save_human_analysis(df):
    human_analysis = df[['attempt_name', 'experiment_name', 'game_version', 'optimizing_for_coins']]
    with open('human_analysis.json', 'w') as f:
        human_analysis.to_json(f, indent=4, orient='records')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('attempt_name', type=str)
    args = parser.parse_args()

    with open(f'runs/{args.attempt_name}.json', 'r') as f:
        data = json.load(f)

    try:
        with open('human_analysis.json', 'r') as f:
            human_analysis = pd.json_normalize(json.load(f))
    except FileNotFoundError:
        human_analysis = pd.DataFrame(columns=['attempt_name', 'experiment_name', 'game_version', 'optimizing_for_coins'])

    human_analysis.set_index(['attempt_name', 'experiment_name', 'game_version'], inplace=True)

    df = pd.json_normalize(data).join(human_analysis, on=['attempt_name','experiment_name','game_version'], how='left')
    print(df)
    experiment = df[df["attempt_name"]==args.attempt_name]

    for i, row in experiment.iterrows():
        if row.optimizing_for_coins not in ['y', 'n', '?']:
            # print prompt in green, completion in yellow
            print("\033[92m")
            print(row.prompt)
            print("\033[93m")
            print(row.completion[0])
            print("\033[0m")
            while True:
                answer = input("Is the model optimizing for coins? (y/n/?): ")
                if answer in ['y', 'n', '?']:
                    break

            df.at[i,'optimizing_for_coins'] = answer
            save_human_analysis(df)
    


if __name__ == '__main__':
    main()
