import json
from tqdm import tqdm

def step1():
    """
    Extract label and description
    :return:
    """
    label_dict = dict()
    with open("data/label.log") as f:
        for aline in tqdm(f):
            info = aline.strip().split(":")
            ln, content = info[0], info[1]
            ln = int(ln)
            if content.find('"}}')==-1:
                if ln in label_dict:
                    label_dict[ln]["lable_info"].append(content)
                else:
                    label_dict[ln] = {
                        "lable_info": [content],
                        "id": ""
                    }
    json.dump(label_dict, open("data/clean_label.json","w"), indent=3)


def step2():
    """
    Merge id info with the label info
    :return:
    """
    data = json.load(open("data/clean_label.json"))
    new_data = dict()
    lower_data = dict()

    with open("data/id.log") as f:
        for aline in tqdm(f):
            if aline.find(":")!=-1:
                info = aline.strip().split(":")
                ln, content = info[0], info[1]
                ln = ln.strip()
                if ln in data:
                    new_data[ln] = data[ln].copy()
                    new_data[ln]["id"] = content.strip()
                    if new_data[ln]["lable_info"][0].lower() == new_data[ln]["lable_info"][0]:
                        lower_data[ln] = new_data[ln].copy()

    json.dump(new_data, open("data/clean_id_label.json", "w"), indent=3)
    json.dump(lower_data, open("data/clean_id_label_lower.json", "w"), indent=3)
    print("STEP 2: Aligning label data with the id")
    print("Total entries: ", len(new_data))
    print("Total lowercase entries: ", len(lower_data))


def step3():
    """
    remove years and neumerical ids
    """
    print("Step 3: loading data")
    data = json.load(open("data/clean_id_label.json"))
    print("loaded id and labels")
    lower_data = json.load(open("data/clean_id_label_lower.json"))
    print("loaded lowercased entities")
    new_data = dict()
    lower_new_data = dict()
    for k,v in data.items():
        if v["lable_info"][0].isnumeric() or v["lable_info"][0]=="year":
            continue
        else:
            new_data[k] = v.copy()

    for k,v in lower_data.items():
        if v["lable_info"][0].isnumeric() or v["lable_info"][0]=="year":
            continue
        else:
            lower_new_data[k] = v.copy()


    json.dump(new_data, open("data/clean_id_label_noNum.json", "w"), indent=3)
    json.dump(lower_new_data, open("data/clean_id_label_lower_noNum.json", "w"), indent=3)
    print("STEP 3: Removing Num")
    print("Total entries: before-", len(data), "   after-",len(new_data))
    print("Total lowercase entries: before-", len(lower_data), "   after-",len(lower_new_data))


def step4():
    """
    Clean double quotation and trailing coma(,) in the ID
    :return:
    """
    print("loading data")
    data = json.load(open("data/clean_id_label_noNum.json"))
    new_data = json.load(open("data/clean_id_label_lower_noNum.json"))
    print("loaded data")
    data_v2 = dict()
    new_data_v2 = dict()

    for k, v in data.items():
        aval = v.copy()
        aval["id"] = aval["id"].replace("\"", '')
        aval["id"] = aval["id"][:len(aval["id"]) - 1].strip()
        data_v2[k] = aval.copy()
    print("processing lowercase ....")
    for k, v in new_data.items():
        aval = v.copy()
        aval["id"] = aval["id"].replace("\"", '')
        aval["id"] = aval["id"][:len(aval["id"]) - 1].strip()
        new_data_v2[k] = aval.copy()
    print("done processing")
    json.dump(data_v2, open("data/clean_id_label_noNum.json", "w"), indent=3)
    json.dump(new_data_v2, open("data/clean_id_label_lower_noNum.json", "w"), indent=3)
    print("saved file")

if __name__=="__main__":
    step1()
    step2()  # extract id
    step3()  # remove numerical entities
    step4()  # rmove trailing coma and double quotation in the ids
