"""
Module to create a custom training dataset for relation extraction based on an LLM. Here, 
we want to extract triplets in german, for that, download the german subpart of the dataset
from the MREBEL model on the hugging face hub (german only)
https://huggingface.co/datasets/Babelscape/SREDFM
It then prepares the dataset with the given prompt
"""
from copy import deepcopy
from src.utils.loaders import prepare_finetunedata
from src.utils.prompts import prompt_dict

if __name__ == '__main__':
    prompt_dict_base = deepcopy(prompt_dict['extraction_tuned'])
    prompt_dict_base.pop(-1)
    prompt_dict_base.pop(-1)
    fine_tuned = prepare_finetunedata(input_path='customds/mrebel_de.jsonl',
                                  instruction_prompt=prompt_dict_base, 
                                  set_size=100000)
    
    fine_tuned.save_to_disk('customds/mrebel_data_100000k.hf')