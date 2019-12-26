import posgres_connect as ps
import get_scores as score_getter
import get_items as items_getter
import csv
import util

def organize_score(thescores, theitems, theresponses ):
    for testid, scoredata in thescores.items():

        responsedict = theresponses[testid]
        for score in scoredata.values():
            if score["itemid"] in items:
                response = responsedict[score["scoreid"]]
                itemdict = theitems[score["itemid"]]
                score["item_pool"] = itemdict["type"]
                score["item_code"] = itemdict["type"] + "_" + itemdict["major"]
                score["item_type"] = itemdict["dtype"]
                score["major"] = itemdict["major"]
                score["poolid"] = util.item_or_empty(response,"poolid")
                score["responseid"] = response["responseid"]
                win_lose = score_getter._win_lose_attribute(response["responseid"], response_attributes)
                process_win_lose(score, items_pooled, win_lose)
                score["ipsative_result"] = win_lose

            else:
                print("Missing item:" + str(score["itemid"]))




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
            score_dict["loser"] = pool + "_" + loser(win_lose)
        elif " lost" in win_lose:
            score_dict["loser"] = score_dict["item_code"]
            score_dict["winner"] = pool + "_" + winner(win_lose)
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


conn = ps.get_connection()
items = items_getter.get_items(conn)
items_pooled = items_by_pool(items)
properties = score_getter.get_property_values(conn)
scores = score_getter.get_scores(conn)
responses = score_getter.get_responses(conn)
response_attributes = score_getter.get_response_attributes(conn)
organize_score(scores,items, responses)
items_getter.save_csv(items)
save_results(scores)

ps.close_connection(conn)
