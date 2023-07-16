# convert json file to csv file
import json
from googletrans import Translator
from tqdm import tqdm
import argparse
from joblib import Parallel, delayed

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_text', default="test.json")
    parser.add_argument('--file_name_save', default='dev_vi.json')
    args = parser.parse_args()
    return args

def main():
    args = config()
    json_file = args.file_text

    with open(json_file, 'r', encoding='utf8') as f:
        data = json.load(f)

    dialog_ids = [i['QuAC_dialog_id'] for i in data]
    print(len(set(dialog_ids)))

    total_batch = divide_batch(data)

    results = Parallel(n_jobs=-1, prefer="threads")(delayed(translate_batch)(i) for i in tqdm(total_batch[:100]))

    final_result = []
    for x in results:
        final_result.extend(x)

    with open(args.file_name_save, 'w', encoding='utf8') as f:
        json.dump(final_result, f)

def divide_batch(data):
    temp_dialog_id = data[0]['QuAC_dialog_id']
    start_idx = 0
    total_batch = []
    for i in tqdm(range(len(data))):
        if data[i]['QuAC_dialog_id'] != temp_dialog_id:
            temp_dialog_id = data[i]['QuAC_dialog_id']
            end_idx = i
            batch_same = data[start_idx:end_idx]
            total_batch.append(batch_same)
            start_idx = i
            continue
    return total_batch

def translate_batch(data):
    translator = Translator(service_urls = ["translate.googleapis.com"])
    temp = []
    total_result = []
    for idx in range(len(data)):
        dict_ = {}
        if idx == 0:
            for history in data[0]['History']:
                temp.append(translator.translate(history, dest='vi').text)
            dict_['History'] = temp
            dict_['QuAC_dialog_id'] = data[0]['QuAC_dialog_id']
            dict_['Question_no'] = data[0]['Question_no']
            dict_['Question'] = translator.translate(data[0]['Question'], dest='vi').text
            dict_['Rewrite'] = translator.translate(data[0]['Rewrite'], dest='vi').text
            total_result.append(dict_)
        else:
            dict_['History'] = total_result[-1]['History'] + [translator.translate(data[idx]['History'][-1], dest='vi').text]
            dict_['QuAC_dialog_id'] = data[0]['QuAC_dialog_id']
            dict_['Question_no'] = data[idx]['Question_no']
            dict_['Question'] = translator.translate(data[idx]['Question'], dest='vi').text
            dict_['Rewrite'] = translator.translate(data[idx]['Rewrite'], dest='vi').text
            total_result.append(dict_)
    return total_result

if __name__ == "__main__":
    main()