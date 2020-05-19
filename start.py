import posgres_connect as ps
import get_scores as score_getter
import get_items as items_getter
import csv
import util

def organize_score(thescores, theitems, theresponses, connection ):

    count = 0
    for testid, scoredata in thescores.items():

        count = count + 1
        if count % 100 == 0:
            print("o_s " + str(count))

        responsedict = theresponses[testid]
        for score in scoredata.values():
            if score["itemid"] in items:
                response = responsedict[score["scoreid"]]
                itemdict = theitems[score["itemid"]]
                score["item_pool"] = itemdict["type"]
                score["item_code"] = itemdict["item_code"]
                score["item_type"] = itemdict["dtype"]
                score["item_genre"] = itemdict["item_genre"]
                score["major"] = itemdict["major"]
                score["poolid"] = util.item_or_empty(response,"poolid")
                score["responseid"] = response["responseid"]
                win_lose = score_getter._win_lose_attribute(response["responseid"], response_attributes)
                process_win_lose(score, items_pooled, win_lose)
                score["ipsative_result"] = win_lose
            elif score["itemid"] in demographics.keys():
                response = responsedict[score["scoreid"]]
                itemdict = demographics[score["itemid"]]
                score["item_type"] = itemdict["dtype"]
                score["item_pool"] = "demographics"
                score["item_code"] = "DMG_" + str(score["itemid"])
                score["score"] = get_response(response["shortresponse"])

            else:
                print("Missing item:" + str(score["itemid"]))

def get_response(optionid):
    if optionid:
        the_options = options
        if int(optionid) in the_options.keys():
            response = the_options[int(optionid) ]
            return response["option"]

    return ""







def items_by_pool(item_dict):
    new_dict = {}

    for key, item_dict in item_dict.items():
        if item_dict["type"] in new_dict.keys():
            pool_dict = new_dict[item_dict["type"]]
        else:
            pool_dict = {}
            new_dict[item_dict["type"]] = pool_dict
        pool_dict[item_dict["id"]] = item_dict
    return new_dict


def loser(win_lose):
    array = win_lose.split(" over ")
    return array[1].strip()


def winner(win_lose):
    array = win_lose.split(" lost to ")
    return array[1].strip()


def process_win_lose(score_dict, item_dict, win_lose):
    if score_dict["item_type"] == "CATSelectableItem":
        pool = score_dict["item_pool"]
        pool_dict = item_dict[pool]
        if " over " in win_lose:
            score_dict["winner"] = score_dict["item_code"]
            score_dict["loser"] = items_getter.make_item_code(pool,loser(win_lose),"")
        elif " lost" in win_lose:
            score_dict["loser"] = score_dict["item_code"]
            score_dict["winner"] = items_getter.make_item_code(pool, winner(win_lose),"")
    else:
        score_dict["loser"] = ""
        score_dict["winner"] = ""


def save_results(scores):
    with open("results.csv", "w", newline='') as f:
        w = csv.writer(f)
        header = ["scoreid", "testtype", "testid", "date", "itemid", "score","item_pool","item_code","item_type","major","responseid","pool_id","ipsative_result","winner","loser"]
        w.writerow(header)
        for testkey, testscores in scores.items():
            for scoreid, score in testscores.items():
                w.writerow([score["scoreid"],
                            score["testtype"],
                            score["testid"],
                            str(score["created"]),
                            score["itemid"],
                            score["score"],
                            util.item_or_empty(score,"item_pool"),
                            util.item_or_empty(score,"item_code"),
                            util.item_or_empty(score,"item_type"),
                            util.item_or_empty(score,"major"),
                            util.item_or_empty(score,"poolid"),
                            util.item_or_empty(score,"responseid"),
                            util.item_or_empty(score,"ipsative_result"),
                            util.item_or_empty(score,"winner"),
                            util.item_or_empty(score,"loser"),
                            ])


def save_flat_results(flat_scores, headers):
    with open("flat_results.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for testkey, testscores in flat_scores.items():

            row = []
            for header in headers:
                row.append(str(value_or_empty(testscores, header)))
            w.writerow(row)

def value_or_empty(dict, key):
    if key in dict.keys():
        return dict[key]
    else:
        ""

def make_flat_dict(test_items):
    flat_dict = {}
    flat_dict["0_usertestid"] = ""
    flat_dict["0_testid"] = ""
    for key, itemdict in test_items.items():
        flat_dict[itemdict["item_code"] + "_itemid"] = ""
        flat_dict[itemdict["item_code"] + "_score"] = ""
        flat_dict[itemdict["item_code"] + "_xwinner"] = ""
        flat_dict[itemdict["item_code"] + "_xloser"] = ""
        flat_dict[itemdict["item_code"] + "_major"] = ""
        flat_dict[itemdict["item_code"] + "_genre"] = ""
    return flat_dict


def include_result(score):
    if "item_type" in score.keys() and "ikert" in score["item_type"]:
        return True

    elif "score" in score.keys():
        return True

    else:
        print(str(score["itemid"]))
        return False

def organize_results_flat(scores, test_items):
    all_flat_results = {}
    count = 0
    for testkey, testscores in scores.items():
        count = count + 1
        if count % 100 == 0:
            print(str(count))

        flat_dict = make_flat_dict(test_items)
        flat_dict["0_usertestid"] = testkey
        flat_dict["0_testid"] = ""

        for scoreid, score in testscores.items():

            if include_result(score):
                if "item_code" in score.keys():
                    flat_dict["0_testid"]  = score["testid"]
                    flat_dict[score["item_code"] + "_itemid"] = score["itemid"]
                    flat_dict[score["item_code"] + "_major"] = value_or_empty(score,"major")
                    flat_dict[score["item_code"] + "_genre"] = value_or_empty(score,"item_genre")
                    flat_dict[score["item_code"] + "_score"] = score["score"]

                    if "elect" in score["item_type"]:
                        flat_dict[score["item_code"] + "_xwinner"] = value_or_empty(score,"winner")
                        flat_dict[score["item_code"] + "_xloser"] = value_or_empty(score, "loser")
                        if score["score"] == 0:
                            flat_dict[score["item_code"] + "_score"] = ""


        all_flat_results[testkey] = flat_dict
    return all_flat_results


def get_flat_headers(flat_result_dict):
    keys = list(flat_result_dict.keys())
    size = len(flat_result_dict)
    headers = list(flat_result_dict[keys[size-1]].keys())
    return sorted(headers)




conn = ps.get_connection()
print("Getting items")
demographics = items_getter.get_demographics(conn)
options = items_getter.get_options(conn)
items = items_getter.get_items(conn)
print("getting items by pool")
items_pooled = items_by_pool(items)
print("Getting scores")
scores = score_getter.get_scores(conn)
print("Getting responses")
responses = score_getter.get_responses(conn)
print("Getting response attributes")
response_attributes = score_getter.get_response_attributes(conn)
print("Organizing scores")
organize_score(scores,items, responses, conn)

items_getter.save_csv(items)
print("Flattening")
flat_results = organize_results_flat(scores, items)
flat_headers = get_flat_headers(flat_results)
print("Saving")
save_flat_results(flat_results, flat_headers)
save_results(scores)


ps.close_connection(conn)
