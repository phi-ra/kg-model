"""
Helper functions to create a training set
"""
from tqdm import tqdm
from copy import deepcopy
from multiprocessing import cpu_count
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer

def apply_chat_template(example, tokenizer):
    messages = example["messages"]
    if messages[0]["role"] != "system":
        messages.insert(0, {"role": "system", "content": ""})
    example["text"] = tokenizer.apply_chat_template(messages, tokenize=False)

    return example

def set_tokenizer(model_id = "mistralai/Mistral-7B-Instruct-v0.1", 
                  cut_length=2048):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token_id is None:
       tokenizer.pad_token_id = tokenizer.eos_token_id
    if tokenizer.model_max_length > 100_000:
       tokenizer.model_max_length = cut_length

    tokenizer.chat_template =  "{% for message in messages %}\n{% if message['role'] == 'user' %}\n{{ '<|user|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'system' %}\n{{ '<|system|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'assistant' %}\n{{ '<|assistant|>\n'  + message['content'] + eos_token }}\n{% endif %}\n{% if loop.last and add_generation_prompt %}\n{{ '<|assistant|>' }}\n{% endif %}\n{% endfor %}"
    return tokenizer

def prepare_finetunedata(input_path, 
                         instruction_prompt, 
                         model_id="mistralai/Mistral-7B-Instruct-v0.1", 
                         cut_length=2048,
                         test_size=0.2,
                         set_size=None,
                         ):
    data_set = load_dataset('json', data_files=input_path)
    print('finished loading')

    full_return = []
    set_counter = 0
    for training_idx in tqdm(range(len(data_set['train']['docid']))):
        if set_size:
            if set_counter >= set_size:
                continue

        current_training_ex = data_set['train'][training_idx]
        
        instr_prompt = deepcopy(instruction_prompt)
        instr_prompt.append({"role": "user", "content": current_training_ex['text']})

        try:
            prompt_list = '['
            for rel_ in current_training_ex['relations']:
                node_1 = rel_['subject']['surfaceform']
                node_2 = rel_['object']['surfaceform']
                edge = rel_['predicate']['surfaceform']
                prompt_list += f'({node_1}, {node_2}, {edge}), '

            final_return = prompt_list[:-2] + ']'
            instr_prompt.append({"role": "assistant", "content": final_return})
        except:
            instr_prompt.append({"role": "assistant", "content": ""})
            
        dict_curr = {"prompt_id": training_idx, "messages": instr_prompt}
        
        full_return.append(dict_curr)
        set_counter += 1

    hf_dataset = Dataset.from_list(full_return)
    tokenizer = set_tokenizer(model_id=model_id, 
                              cut_length=cut_length)

    raw_dataset = hf_dataset.map(apply_chat_template,
                                 num_proc=(cpu_count()-1),
                                 fn_kwargs={"tokenizer": tokenizer},
                                 desc="Applying chat template")
    
    raw_dataset = raw_dataset.train_test_split(test_size)

    return raw_dataset