import csv


testcontentelement_columns = {}
testcontentelement_columns["id"] = 0
testcontentelement_columns["stem"] = 1
testcontentelement_columns["prompt"] = 2
testcontentelement_columns["category"] = 3
testcontentelement_columns["temp"] = 4
testcontentelement_columns["major"] = 5


items_query = "select tce.id, tce.stem, tce.prompt, tcep.contentelementtypepropertykey, " \
              "cetp.value, tce.dtype from testcontentelement tce " \
              "INNER JOIN testcontentelementcetpropertyvalue tcep " \
              "ON tce.id = tcep.testcontentelementid " \
              "INNER JOIN contentelementtypeproperty cetp " \
              "ON tcep.contentelementtypepropertyid = cetp.id " \
              "where tcep.contentelementtypepropertykey like" \
              " '%cet_property_cati_msproperties_assessed_category%'" \
              "and cetp.value NOT LIKE '%HI_%' order by tce.id;"

def row_to_dict(row, dict, keylist):
    return_dict = {}
    for key in keylist:
        return_dict[key] = str(row[dict[key]])
    return return_dict


def is_item_type(row):
    value = row[4]
    if "R0" in value:
        return True
    elif "H1" in value:
        return True
    else:
        return False


def get_items(connection):
    cursor = connection.cursor()
    cursor.execute(items_query)
    rows = cursor.fetchall()
    results = {}
    count = 1
    for row in rows:
        if row[0] in results.keys():
            if is_item_type(row):
                results[row[0]]["type"] = row[4]
            else:
                results[row[0]]["major"] = results[row[0]]["major"] + " " + str(row[4])

        else:
            row_dict = {}
            row_dict["id"] = row[0]
            row_dict["stem"] = row[1]
            row_dict["prompt"] = row[2]

            row_dict["type"] = ""
            row_dict["major"] = ""
            if is_item_type(row):
                row_dict["type"] = row[4]
            else:
                row_dict["major"] = row[4]
            row_dict["dtype"] = row[5]
            results[row[0]] = row_dict

        count = count + 1
    return results



def save_csv(dict):
    with open("items.csv", "w", newline='') as f:
        w = csv.writer(f)
        thekeys = list(dict.keys())
        header = list(dict[thekeys[0]].keys())
        w.writerow(header)
        for key in thekeys:
            row = dict[key]
            w.writerow([row["id"],row["stem"],row["prompt"],row["type"],row["major"],row["dtype"]])