
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)
import argparse
import torch

from flask import Flask,request
app= Flask(__name__)

def parse_args():
    parser= argparse.ArgumentParser()
    parser.add_argument("--device", type =str, default ="-1")
    return parser.parse_args()


@torch.inference_mode()
def process(content):
    content = content.lower()
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


@app.route('/address', methods =['GET','POST'])
def generate_keyword():
    content = request.json['address']
    key_gen, scores = process(content )
    return {
        'res': key_gen,
        'scores': scores
    }

if __name__ == '__main__':
    args = parse_args()
    if args.device != "-1" and torch.cuda.is_available():
        device = torch.device(f"cuda:{args.device}")
    else:
        device = torch.device("cpu")
    model = AutoModelForSeq2SeqLM.from_pretrained("weights/address_v1_vit5_base")
    model.to(device)
    tokenizer = AutoTokenizer.from_pretrained("weights/address_v1_vit5_base")
    model.eval()
    
    # dummy input
    content ="thon 6, lưỡng vương, tp tuyên quang"
    process(content)

    print("Model Loaded")
    app.run(host='0.0.0.0', port=3499, debug=False)