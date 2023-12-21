from io import BytesIO
import json
import threads
from meta_assistants.assistants import all_assitants
import time

fine_tuning_model = 'gpt-3.5-turbo-1106'

def finetuning_phase1(inp, pe) -> str:
    """
    Fine-tunes and returns a model id.
    """
    file = BytesIO()
    system_prompt = all_assitants['gradient_hacker_v1']['instructions']
    for item in inp:
        file.write(json.dumps({
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },{
                    "role": "user",
                    "content": item['phase1_prompt']
                },{
                    "role": "assistant",
                    "content": item['phase1_suggested_completion']
                }
            ]
        }).encode('utf-8'))
        file.write(b'\n')

    # Call OpenAI's fine tuning API
    print("Uploading file to OpenAI")
    client = threads.client
    file_id = client.files.create(
        file=('gh1_coins.jsonl', file.getvalue(), 'application/jsonl'),
        purpose="fine-tune"
    ).id
    print(f"File id is {file_id}")

    print("Calling OpenAI's fine tuning API")
    stuff = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=fine_tuning_model,
        hyperparameters={
            'n_epochs':20,
        })
    job_id = stuff.id
    print(f"Job id is {job_id}")

    print("Waiting for fine tuning to complete")
    while True:
        stuff = client.fine_tuning.jobs.retrieve(job_id)
        print(stuff)
        if stuff.status in ['succeeded','failed','cancelled']:
            model_id = stuff.fine_tuned_model
            print(f"Model id is {model_id}")
            return model_id
        time.sleep(5)