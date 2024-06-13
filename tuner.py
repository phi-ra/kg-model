from datasets import load_from_disk
from peft import LoraConfig
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer
import yaml

if __name__ == '__main__':

    with open('conf/public/tuneparams.yml') as con:
        params = yaml.safe_load()

        # storage
        model_id = params['data']['pretrained']
        tokenizer_id = params['data']['tokenizer']
        datset_id = params['data']['traindata']
        output_dir = params['data']['checkpoints']

        # train hyper
        lr = params['hyper']['lr']
        total_ep = params['hyper']['epochs']
        logging_steps = params['hyper']['logging']


        # load saved datasets (otherwise run )
        raw_datasets = load_from_disk(datset_id)

        quantization_config = BitsAndBytesConfig(
                load_in_4bit= params['hyper']['4bitquant'],
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype= params['hyper']['floattype'],
    )
        device_map = {"": torch.cuda.current_device()} if torch.cuda.is_available() else None

        model_kwargs = dict(
            torch_dtype="auto",
            use_cache=False, 
            device_map=device_map,
            quantization_config=quantization_config,
        )

        peft_config = LoraConfig(
                r = params['hyper']['attentiondim'],
                lora_alpha = params['hyper']['scaling'],
                lora_dropout = params['hyper']['dropout'],
                bias = 'none',
                task_type = "CAUSAL_LM",
                target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
        )

        train_dataset = raw_datasets["train"]
        eval_dataset = raw_datasets["test"]

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)

        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id

        if tokenizer.model_max_length > 100_000:
            tokenizer.model_max_length = params['hyper']['max_len']

    # Set chat template
    DEFAULT_CHAT_TEMPLATE = "{% for message in messages %}\n{% if message['role'] == 'user' %}\n{{ '<|user|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'system' %}\n{{ '<|system|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'assistant' %}\n{{ '<|assistant|>\n'  + message['content'] + eos_token }}\n{% endif %}\n{% if loop.last and add_generation_prompt %}\n{{ '<|assistant|>' }}\n{% endif %}\n{% endfor %}"
    tokenizer.chat_template = DEFAULT_CHAT_TEMPLATE


# based on config
    training_args = TrainingArguments(
        fp16=True, 
        do_eval=True,
        evaluation_strategy="epoch",
        gradient_accumulation_steps=32,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        learning_rate=lr,
        log_level="info",
        logging_steps=logging_steps,
        logging_strategy="steps",
        lr_scheduler_type="cosine",
        max_steps=-1,
        num_train_epochs=total_ep,
        output_dir=output_dir,
        overwrite_output_dir=True,
        per_device_eval_batch_size=1,
        per_device_train_batch_size=1,
        push_to_hub=False,
        report_to="wandb",
        save_strategy="no",
        save_total_limit=None,
        seed=42,
    )

    trainer = SFTTrainer(
            model=model_id,
            model_init_kwargs=model_kwargs,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            dataset_text_field="text",
            tokenizer=tokenizer,
            packing=True,
            peft_config=peft_config,
            max_seq_length=tokenizer.model_max_length,
        )
    train_result = trainer.train()

        