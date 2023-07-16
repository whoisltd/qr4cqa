from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    LogitsProcessorList,
    MinLengthLogitsProcessor,
    BeamSearchScorer,
    PhrasalConstraint,
    MBartForConditionalGeneration,
)
import time
import torch
torch.cuda.set_device(0)
import pandas as pd

model = AutoModelForSeq2SeqLM.from_pretrained("weights/address_v1_vit5_base")
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
model.to(device)
tokenizer = AutoTokenizer.from_pretrained("weights/address_v1_vit5_base")
model.eval()

@torch.inference_mode()
def generate_keyword(content):
    unique_keyword = set()
    inputs = tokenizer.batch_encode_plus([content], padding='max_length', truncation=True, max_length=256, return_tensors='pt')

    outputs = model.generate(inputs.input_ids.to(device),
                             attention_mask = inputs.attention_mask.to(device),
                             max_length = 256,
                             early_stopping= True,
                             num_return_sequences=3,
                             typical_p = 0.9,
                             num_beams=3, return_dict_in_generate=True, output_scores=True)
    scores = torch.nn.functional.softmax(outputs.sequences_scores)
    key_gen = tokenizer.batch_decode(outputs.sequences, skip_special_tokens=True)
    return key_gen, scores

content ="thon 6, lưỡng vương, tp tuyên quang"
generate_keyword(content)

start = time.time()
content ="thon 6, lưỡng vương, tp tuyên quang"
print('Raw Address:', content)
print('Address:', generate_keyword(content))
print('Time:', time.time() - start)
