# convert json file to csv file
import json
from googletrans import Translator
from tqdm import tqdm
import argparse
from joblib import Parallel, delayed

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_text', default="dev.json")
    parser.add_argument('--file_name_save', default='dev_vi.json')
    args = parser.parse_args()
    return args

def main():
    args = config()
    json_file = args.file_text

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dialog_ids = [i['QuAC_dialog_id'] for i in data]
    print(len(set(dialog_ids)))

    total_batch = divide_batch(data)

    results = Parallel(n_jobs=-1, prefer="threads")(delayed(translate_batch)(i) for i in tqdm(total_batch))

    # final_result = []
    # for x in results: final_result.extend(x)
    final_result = combine_batches(results)

    with open(args.file_name_save, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False)

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
    total_result = []
    temp_his_trans = {data[-1]['History'][index]: value.text for index, value in enumerate(translator.translate(data[-1]['History'], dest='vi'))}

    for idx in range(len(data)):
        dict_ = {}
        dict_['History'] = [temp_his_trans[key] for key in data[idx]['History']]
        dict_['QuAC_dialog_id'] = data[idx]['QuAC_dialog_id']
        dict_['Question_no'] = data[idx]['Question_no']
        dict_['Question'] = temp_his_trans[data[idx]['Question']] if data[idx]['Question'] in temp_his_trans else translator.translate(data[idx]['Question'], dest='vi').text
        dict_['Rewrite'] = translator.translate(data[idx]['Rewrite'], dest='vi').text
        total_result.append(dict_)
    return total_result

def combine_batches(results):
    final_result = []
    for x in results: final_result.extend(x)
    return final_result

if __name__ == "__main__":
    main()