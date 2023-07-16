import base64
import re
import unicodedata
import xml.etree.ElementTree as etree
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from vncorenlp import VnCoreNLP

rdrsegmenter = VnCoreNLP(
    "./VnCoreNLP/VnCoreNLP-1.2.jar", annotators="wseg,pos", max_heap_size="-Xmx2g"
)

def preprocess_content(content):
    punc = """#@*\^~"""
    soup = BeautifulSoup(content, "html.parser")
    for data in soup(["style", "script", "code", "a"]):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    text = soup.get_text()
    text = unicodedata.normalize("NFKC", text)
    text = re.sub("\n", " . ", text)
    text = re.sub("&#038", " ", text)
    text = re.sub("[?|!]", "..", text)
    text = re.compile("[%s]" % re.escape(punc)).sub(" ", text)
    text = re.sub("\s+", " ", text)
    text = rdrsegmenter.tokenize(text)
    for list_word in text:
        if list_word[len(list_word) - 1] != ".":
            list_word.insert(len(list_word), ".")
        for i, word in enumerate(list_word):
            if word == "." and i != (len(list_word) - 1):
                list_word.pop(i)
    text = " ".join(" ".join(doc) for doc in text if doc != ["."])
    text = re.sub("[.]{2,}", " ", text)
    text = re.sub("\s+", " ", text)
    
    return text

def gg_suggest(query):
    r = requests.get(
        "http://www.google.com/complete/search",
        params={
            "q": query,
            "hl": "vn",
            "ie": "utf_8",
            "oe": "utf_8",
            "output": "toolbar",
        },
    )
    root = etree.XML(r.text)
    sugs = root.xpath("//suggestion")
    sugstrs = [s.get("data") for s in sugs]
    return sugstrs


def show_result_kw_ggtrends(list_kw):
    pytrend = TrendReq(hl="vietnam", proxies=["http://10.3.51.70:6210"], retries=5)
    
    # provide your search terms
    kw_list = list_kw
    pytrend.build_payload(kw_list, timeframe="now 1-d", geo="VN")
    # Interest by time
    regiondf = pytrend.interest_over_time()
    # drop all rows that have null values in all columns
    regiondf.dropna(how="all", axis=0, inplace=True)
    regiondf.index = regiondf.index + pd.DateOffset(hours=7)
    if regiondf.empty:
        return pd.DataFrame()
    else:
        regiondf.drop(columns=["isPartial"], inplace=True)
        return regiondf


def find_unique_word(list_token, set_unique_keywords):
    unique_keywords = set_unique_keywords
    i = 0
    while i < len(list_token):
        if "N" in list_token[i]["posTag"]:
            tg = i + 1
            phrase_noun = [list_token[i]["form"].lower()]
            while tg < len(list_token):
                if "N" in list_token[tg]["posTag"]:
                    phrase_noun.append(list_token[tg]["form"].lower())
                    tg += 1
                    continue
                if "M" in list_token[tg]["posTag"]:
                    phrase_noun.append(list_token[tg]["form"].lower())
                    break
                if ("M" not in list_token[tg]["posTag"]) and (
                        "N" not in list_token[tg]["posTag"]
                ):
                    break
            if len(phrase_noun) == 1:
                if list_token[i]["posTag"] == "Np":
                    unique_keywords.add(" ".join(phrase_noun))
                elif (list_token[i]["posTag"] != "Np") and (i == 0):
                    unique_keywords.add(" ".join(phrase_noun))
                elif (
                        (list_token[i]["posTag"] == "N")
                        and (i != 0)
                        and (re.search("_", list_token[i]["form"]) is True)
                ):
                    unique_keywords.add(" ".join(phrase_noun))
                i = tg
                
            else:
                unique_keywords.add(" ".join(phrase_noun))
                i = tg + 1

        elif (list_token[i]["posTag"] == "V") and (
                re.search("_", list_token[i]["form"])
        ):
            unique_keywords.add(list_token[i]["form"].lower())
            i += 1
        else:
            i += 1

    return unique_keywords



def post_processing(list_result):
    title_one = re.sub("[.]$", "", list_result[0])
    title_one = re.sub("_", " ", title_one)
    final_result = [title_one]
    title_one = title_one.strip()
    unique_keywords = set()

    list_word_title_one = rdrsegmenter.annotate(title_one)["sentences"][0]
    refer_postag = [list_word_title_one[0]["posTag"]]
    unique_keywords = find_unique_word(list_word_title_one, unique_keywords)

    for title in list_result[1:]:
        if len(final_result) == 3:
            break
        title = re.sub("[.]$", "", title)
        title_after = re.sub("_", " ", title)
        title_after = title_after.strip()
        seperate_title = rdrsegmenter.annotate(title_after)["sentences"][0]

        if seperate_title[0]["posTag"] not in refer_postag:
            refer_postag.append(seperate_title[0]["posTag"])
            unique_keywords = find_unique_word(seperate_title, unique_keywords)
            final_result.append(title_after)
        else:
            temp_unique_keyword = set()
            temp_unique_keyword = find_unique_word(seperate_title, temp_unique_keyword)
            for token in temp_unique_keyword:
                if token not in unique_keywords:
                    unique_keywords.add(token)
                    if title_after in final_result:
                        continue
                    else:
                        final_result.append(title_after)

    for title in list_result:
        if len(final_result) == 3:
            break

        title = re.sub("[.]$", "", title)
        title = re.sub("_", " ", title)
        if title not in final_result:
            final_result.append(title)
            
    all_token = set()
    unique_words_other = set()
    
    for title in final_result:
        punctuation = """!"#$%&'()’’*+,-/:;’’’’”…<=>’?’@[]\^_`{|}~°®”€“"""
        title_after = re.compile("[%s]" % re.escape(punctuation)).sub(
            " ", title
        )  # remove punctuation
        title_after = title_after.strip()
        title_after = re.sub(" +", " ", title_after)
        list_word = rdrsegmenter.annotate(title_after)["sentences"][0]
        for token in list_word:
            all_token.add(token["form"].lower())

    concat_word_sent = " ".join(list(unique_keywords))
    list_token_in_unique_word_final = concat_word_sent.split(" ")
    for token in all_token:
        if token not in list_token_in_unique_word_final:
            unique_words_other.add(token)

    unique_word = [re.sub("_", " ", word) for word in list(unique_keywords)]
    unique_words_other = [re.sub("_", " ", word) for word in unique_words_other]

    return final_result, unique_word, unique_words_other


def show_chart_ggtrend(keywords):
    list_kw = []
    i = 0
    while i < len(keywords):
        list_kw.append(keywords[i: i + 5])
        i += 5

    kw_data = pd.DataFrame()
    for kw in list_kw:
        result_df = show_result_kw_ggtrends(kw)
        if kw_data.empty:
            kw_data = pd.concat([kw_data, result_df], axis="rows")
        else:
            if result_df.empty:
                kw_data = kw_data
            else:
                kw_data = pd.merge(kw_data, result_df, on="date")
    kw_data = kw_data.reindex(kw_data.mean().sort_values().index, axis=1)
    data_bar = kw_data.mean().to_frame().T

    try:
        timeseriese_plot = kw_data.plot(
            figsize=(10, 6), y=list(kw_data.columns), kind="line"
        )
        plt.legend(
            [
                colum + f" ({kw_data[str(colum)].mean():.2f}) "
                for colum in list(kw_data.columns)
            ]
        )
        timeseriese_plot = timeseriese_plot.figure
        timeseriese_plot.savefig("timeseriese_plot.jpg")
        plt.close(timeseriese_plot)
        image_timeseriese = cv2.imread("timeseriese_plot.jpg")
    except:
        image_timeseriese = np.full((10, 6, 3), 255, dtype=np.uint8)
    image_timeseriese = base64.b64encode(
        cv2.imencode(".jpg", image_timeseriese)[1]
    ).decode("utf-8")

    try:
        bar_plot = data_bar.plot(figsize=(10, 6), y=list(data_bar.columns), kind="bar")
        bar_plot = bar_plot.figure
        bar_plot.savefig("bar_plot.jpg")
        plt.close(bar_plot)
        bar_plot = cv2.imread("bar_plot.jpg")
    except:
        bar_plot = image_timeseriese = np.full((10, 6, 3), 255, dtype=np.uint8)

    bar_plot = base64.b64encode(cv2.imencode(".jpg", bar_plot)[1]).decode("utf-8")
    return image_timeseriese, bar_plot


def processing_pos_tag_kw(list_kw):
    """
    It takes a list of results and returns a list of results.
    :param list_kw: list of keywords
    """
    final_result = []
    for kw in list_kw:
        kw_after = []
        annot = rdrsegmenter.annotate(kw)['sentences'][0]
        i=0
        while i < len(annot):
            if annot[i]['posTag'] == "M":
                if i+1 < len(annot):
                    if annot[i+1]['posTag'] in ["Nc", "N"]:
                        i +=2
                        continue
                    else:
                        kw_after.append(annot[i]['form'])
                else:
                     kw_after.append(annot[i]['form'])
            elif annot[i]['posTag'] == "N":
                if i+2 < len(annot):
                    if (annot[i+1]['posTag'] == "Np") and (annot[i+2]['posTag'] == "Np"):
                        i +=2
                        continue
                    else:
                        kw_after.append(annot[i]['form'])
                else:
                     kw_after.append(annot[i]['form'])
            elif annot[i]['posTag'] == "A":
                if i == 0 or i == len(annot) -1:
                    kw_after.append(annot[i]['form'])
                else:
                    i +=1
                    continue
            elif annot[i]['posTag'] not in ["Nc", "P", "C", "Cc", "X", "Ny", "Z"]:
                kw_after.append(annot[i]['form'])
            i +=1
        keyword = re.sub("_", " ", " ".join(kw_after))
        final_result.append(keyword)

    return list(set(final_result))


def get_ip():
    """
    It returns the IP address of the machine.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.connect(('10.255.255.255', 1))
        ip_address = client.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'
    finally:
        client.close()

    return ip_address
