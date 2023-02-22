import torch
from transformers import BloomTokenizerFast
from petals import DistributedBloomForCausalLM

# MODEL_NAME = "bigscience/bloom-petals"
MODEL_NAME = "bloom-petals"
tokenizer = BloomTokenizerFast.from_pretrained(MODEL_NAME)
model = DistributedBloomForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
model = model.cpu()

# model = model.cuda()
inputs = tokenizer('Best USA president was', return_tensors="pt")["input_ids"].cpu()
outputs = model.generate(inputs, max_new_tokens=10)
print(tokenizer.decode(outputs[0]))
