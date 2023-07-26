# convert json file to csv file
import argparse
import json
import re
from typing import List

from googletrans import Translator
from joblib import delayed
from joblib import Parallel
from tqdm import tqdm

pattern = r"<[^>]*>"


def config():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_text",
        default="/home/pphuc/Coding/Project/qr4cqa/datasets/CANARD_Release/en/dev.json",
    )
    parser.add_argument("--file_name_save", default="dev_vi.json")
    args = parser.parse_args()
    return args


def main():
    args = config()
    json_file = args.file_text

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dialog_ids = [i["QuAC_dialog_id"] for i in data]
    print(len(set(dialog_ids)))

    total_batch = divide_batch(data)

    results = Parallel(n_jobs=-1, prefer="threads")(
        delayed(translate_batch_v2)(i) for i in tqdm(total_batch)
    )

    final_result = combine_batches(results)

    with open(args.file_name_save, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False)


def divide_batch(data: List[dict]) -> List[list]:
    """
    Divide a whole data into each batch according to QuAC_dialog_id,
    in which a batch is a full conversation

    Args:
        data: the whole data containing multiple conversation

    Returns:
        List(list): a list containing many batches
    """
    temp_dialog_id = data[0]["QuAC_dialog_id"]
    start_idx = 0
    total_batch = []
    for i in tqdm(range(len(data))):
        if data[i]["QuAC_dialog_id"] != temp_dialog_id:
            temp_dialog_id = data[i]["QuAC_dialog_id"]
            end_idx = i
            batch_same = data[start_idx:end_idx]
            total_batch.append(batch_same)
            start_idx = i
        if i == len(data) - 1:
            end_idx = i + 1
            batch_same = data[start_idx:end_idx]
            total_batch.append(batch_same)
    return total_batch


# def translate_batch(data: List[dict]) -> List[dict]:
#     translator = Translator(service_urls = ["translate.googleapis.com"])
#     total_result = []
#     temp_his_trans = {data[-1]['History'][index]: value.text for index, value in enumerate(translator.translate(data[-1]['History'], dest='vi'))}

#     for idx in range(len(data)):
#         dict_ = {}
#         dict_['History'] = [temp_his_trans[key] for key in data[idx]['History']]
#         dict_['QuAC_dialog_id'] = data[idx]['QuAC_dialog_id']
#         dict_['Question_no'] = data[idx]['Question_no']
#         dict_['Question'] = temp_his_trans[data[idx]['Question']] if data[idx]['Question'] in temp_his_trans else translator.translate(data[idx]['Question'], dest='vi').text
#         dict_['Rewrite'] = translator.translate(data[idx]['Rewrite'], dest='vi').text
#         total_result.append(dict_)
#     return total_result


def translate_batch_v2(data: List[dict]) -> List[dict]:
    """
    Translate history, questions, rewrites into vietnamese by translate in
    all context

    Args:
        data: A batch data of a conversation

    Parameters:
        temp_his_trans: the dict contain translated conversation history and devided by original question
        temp_question: the dict contain translated conversation question and devided by index
        temp_rewrites: the dict contain translated conversation rewrites and devided by index

    Returns:
        List(list): Translated conversation
    """
    translator = Translator(service_urls=["translate.googleapis.com"])
    total_result = []
    questions_list = [value["Question"] for value in data]
    rewrites_list = [value["Rewrite"] for value in data]

    questions = "   <%%|$|%%>   ".join(questions_list)
    history = "   <%%|$|%%>   ".join(data[-1]["History"])
    rewrites = "   <%%|$|%%>   ".join(rewrites_list)

    temp_his_trans: dict = {
        data[-1]["History"][index]: value.strip()
        for index, value in enumerate(
            re.split(pattern, translator.translate(history, dest="vi").text)
        )
    }
    temp_question: dict = {
        index: value.strip()
        for index, value in enumerate(
            re.split(pattern, translator.translate(questions, dest="vi").text)
        )
    }
    temp_rewrites: dict = {
        index: value.strip()
        for index, value in enumerate(
            re.split(pattern, translator.translate(rewrites, dest="vi").text)
        )
    }

    for idx in range(len(data)):
        dict_ = {}
        dict_["History"] = [temp_his_trans[key] for key in data[idx]["History"]]
        dict_["QuAC_dialog_id"] = data[idx]["QuAC_dialog_id"]
        dict_["Question_no"] = data[idx]["Question_no"]
        dict_["Question"] = (
            temp_his_trans[data[idx]["Question"]]
            if data[idx]["Question"] in temp_his_trans
            else temp_question[idx]
        )
        dict_["Rewrite"] = temp_rewrites[idx]
        total_result.append(dict_)
    return total_result


def combine_batches(results: List[list]) -> list:
    """
    Combine each batch into a single list

    Args:
        results: A List contain multiple list of after preprocess

    Return:
        (list): A single list
    """
    final_result = []
    for x in results:
        final_result.extend(x)
    return final_result


if __name__ == "__main__":
    main()
