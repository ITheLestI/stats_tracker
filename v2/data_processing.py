import requests, json, sys, os
import pyexcel as p
from flask import Flask, render_template, redirect
url = "https://psv4.userapi.com/c236331/u4636527/docs/d60/0b38906fcd06/kontrolnye_starty_2021-2022.xls"
   

app = Flask(__name__)

os.chdir(os.path.dirname(sys.argv[0]))

def download_file():
    book_dict = dict(p.get_book_dict(file_name="data.xls"))
    book_dict.pop("Лист1")
    book_dict.pop("50бр+50вс")
    book_dict.pop("50бт+50сп ")
    
    return format_json(book_dict)


def format_json(input_dict):
    stats = [
      "name",
      "year",
      "prev_points",
      "time",
      "class",
      "got_points",
      "points",
      "place"
    ]
    for distance in input_dict.keys():
        data = input_dict[distance][3:]
        to_pop = []
        for swimmer in range(len(data)):
            data[swimmer].pop(0)
            data[swimmer].pop(3)
            
            if data[swimmer][3] != "" and data[swimmer][3] != "д.к.":
                if isinstance(data[swimmer][3], str) and data[swimmer][3][:-6]:
                    a = int(data[swimmer][3][:-6])
                    b = int(data[swimmer][3][-5:-3])
                    if b < 10:
                        b = "0" + str(b)
                    c = int(data[swimmer][3][-2:])
                    data[swimmer][3] = f"{a}:{b},{c}"
            

            if data[swimmer][1] not in [2007, 2008]:
                 to_pop.append(swimmer)
            
            data[swimmer] = dict(zip(stats, data[swimmer]))
        
            """offset = 0
            for i in to_pop:
                del data[i-offset]
                offset+=1"""

        input_dict[distance] = data
    

    """to_pop = []
    for distance_key in input_dict.keys():
        swimmers = input_dict[distance_key]
        for i in range(len(swimmers)):
            if swimmers[i]["year"] not in [2007, 2008]:
                to_pop.append(i)
        offset = 0
        for i in to_pop:
            del swimmers[i-offset]
            offset+=1

        siwmmers_sorted = sorted(swimmers, key = lambda x: x["place"] if x["place"] != "" else 999999)
        for i in range(len(siwmmers_sorted)):
            siwmmers_sorted[i]["overall_place"] = siwmmers_sorted[i]["place"]
            siwmmers_sorted[i]["place"]=i+1
        input_dict[distance_key] = siwmmers_sorted
        to_pop.clear()"""
    return input_dict    



def main():
    distances = download_file()
    #with open("data.json", "w") as file:
    #    json.dump(distances, file, ensure_ascii=False, indent=2)
    
    
    
    json.dump(distances, open("data2008sorted.json", "w"), ensure_ascii=False, indent=2)

@app.route("/")
def starting_page():
    return main()

@app.route("/<type>")
def mabbb(type="200vs"):
    swimmers = download_file()
    return_val = []
    if type == "200vs":
        return_val = swimmers["200 вс"]
    elif type == "100bt":
        return_val = swimmers["100 бт"]
    elif type == "100sp":
        return_val = swimmers["100 сп "]
    elif type == "100br":
        return_val = swimmers["100 бр"]
    elif type == "100vs":
        return_val = swimmers["100 вс"]
    elif type == "400vs":
        return_val = swimmers["400 вс"]
    elif type == "200kp":
        return_val = swimmers["200 КП "]
    elif type == "100kp":
        return_val = swimmers["100 КП"]

    '''
    match type:
        case "200vs":            
            return_val = swimmers["200 вс"]
        case "100bt":
            return_val = swimmers["100 бт"]
        case "100sp":
            return_val = swimmers["100 сп "]
        case "100br":
            return_val = swimmers["100 бр"]
        case "100vs":
            return_val = swimmers["100 вс"]
        case "400vs":
            return_val = swimmers["400 вс"]
        case "200kp":
            return_val = swimmers["200 КП "]
        case "100kp":
            return_val = swimmers["100 КП"]'''
    if len(return_val) == 0:
        return "Bad adress error"
    return render_template("index.html", table=return_val, type=type)

if __name__ == "__main__":
    main()