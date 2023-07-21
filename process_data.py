import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    DATA_DIR = './datasets/CANARD_Release'
    OUTPUT_DIR = './data'
    
    languages = ['en', 'vi']
    
    splits = ['train', 'dev', 'test']
    
    for language in languages:
        for split in splits:
            if language == 'en':
                filepath = os.path.join(DATA_DIR, language, f'{split}.json')
            else:
                filepath = os.path.join(DATA_DIR, language, f'{split}_vi.json')
            with open(filepath, 'r') as f:
                data = json.load(f)
            inputs = []
            outputs = []
            for dialog in data:
                history = dialog['History']
                question = dialog['Question']
                rewriting = dialog['Rewrite']
                input = ".".join(history) + "." + question
                output = rewriting
                inputs.append(input)
                outputs.append(output)
            df = pd.DataFrame({'input': inputs, 'output': outputs})
            df.to_csv(f'{OUTPUT_DIR}/{language}_{split}.csv')