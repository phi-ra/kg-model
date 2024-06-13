# kg-model 

Repository to fit the LoRA adapter onto Mistral7b, to have a model that gives more consistent outputs. Largely follows the huggingface tutorials with some tweaks here and there. 

## Ideas
To extract triplets from a given text, the core idea is to use an LLM with an adequate prompt that extracts what we need. Since some qualitative evaluations showed that the answers are quite variable, this repository aims at fine-tuning an LLM to give something more consistent. For this, we use the (german) MREBEL dataset which provides both triplets and a context chunk. 

## Usage 
Usage is straightforward, first, run `data_prep.py`, which transforms the data from MREBEL into something we can feed the model over the huggingface adaptations. Then, fine-tune the model on the generated data using `tuner.py`. In theory, it would be best to run this whole routine in a Docker container or something the like, but given that the script is not really robust to changes in the hardware, its provided as a sample script instead (note that most of the code follows different huggingface implementations). Here, the main model used is Mistral 7B. 