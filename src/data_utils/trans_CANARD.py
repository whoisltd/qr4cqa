# convert json file to csv file
import json
from googletrans import Translator
from tqdm import tqdm

translator = Translator()

def main():

    json_file = "dev.json"

    with open(json_file, 'r', encoding='utf8') as f:
        data = json.load(f)

    dialog_ids = [ i['QuAC_dialog_id'] for i in data]

    print(len(set(dialog_ids)))

    #transalte history, question
    # => question add to temp history
    # check history is in temp history
    # if not, translate and add to temp history
    # if yes, continue
    # go to next question in a history, ...


    temp_dialog_id = ''
    temp_history = []
    temp_dict = {}
    vi_diaglog=[]
    for i in tqdm(range(len(data))):
        if data[i]['QuAC_dialog_id'] != temp_dialog_id:
            temp_dialog_id = data[i]['QuAC_dialog_id']
            temp_history = []
            temp_dict = {}
            his_arr = []
        for j in data[i]['History']:
            if j not in temp_history:
                temp_history.append(j)
                translated = translator.translate(j, dest='vi')
                his_arr.append(translated.text)
        
        temp_dict['History'] = his_arr
        temp_dict['QuAC_dialog_id'] = temp_dialog_id
        ques_trans = translator.translate(data[i]['Question'], dest='vi').text
        temp_dict['Question'] = ques_trans
        temp_dict['Question_no'] = data[i]['Question_no']
        temp_dict['Rewrite'] = translator.translate(data[i]['Rewrite'], dest='vi').text
        temp_history.append(data[i]['Question'])
        his_arr.append(ques_trans)
        
        vi_diaglog.append(temp_dict)
# add vi_diaglog array to json file
    with open('dev_vi.json', 'w', encoding='utf8') as f:
        json.dump(vi_diaglog, f)


main()