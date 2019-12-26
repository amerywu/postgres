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
              "and cetp.value NOT LIKE '%HI_%' order by tce.id desc;"
              #"order by tce.id;"


def row_to_dict(row, dict, keylist):
    return_dict = {}
    for key in keylist:
        return_dict[key] = str(row[dict[key]])
    return return_dict

def get_property_values(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.contentelementtypeproperty order by id")
    rows = cursor.fetchall()
    property_dict = {}



    for row in rows:
        row_dict = {}
        row_dict["id"] = row[0]
        row_dict["key"] = row[3]
        row_dict["name"] = row[5]
        row_dict["value"] = row[6]
        property_dict[row[0]] = row_dict
        #print(util.print_row_value(row,contentelementtypeproperty_columns,["id","key","name","value"]))
    return property_dict

def get_property_relations(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.testcontentelementcetpropertyvalue order by id")
    rows = cursor.fetchall()
    property_by_item_dict = {}

    for row in rows:
        item_id = row[5]
        if item_id not in property_by_item_dict.keys():
            item_dict = {}
            property_by_item_dict[item_id] = item_dict

        row_dict = {}
        row_dict["id"] = row[0]
        row_dict["key"] = row[1]
        row_dict["property_id"] = row[4]
        row_dict["item_id"] = row[5]

        property_by_item_dict[item_id][row[4]] = row_dict
        # print(util.print_row_value(row,contentelementtypeproperty_columns,["id","key","name","value"]))
    return property_by_item_dict

def is_item_type(row):
    value = row[4]
    if "R0" in value:
        return True
    elif "H1" in value:
        return True
    else:
        return False

def major(existing, new):
    if not existing:
        return new
    elif "G_" in existing:
        return existing + "_" + new
    else:
        return new + "_" + existing

def add_properties(property_values, property_relations, item):
    item_id = item["id"]
    prelations = property_relations[item_id]
    item["item_genre"] = ""
    for pdict in prelations.values():
        if pdict["key"] == "cet_property_cati_msproperties_assessed_category_C":
            value = property_values[pdict["property_id"]]["value"]
            item["item_genre"] = value
        elif pdict["key"] == "cet_property_cati_msproperties_assessed_category_A":
            value = property_values[pdict["property_id"]]["value"]
            item["major"] = value




def get_items(connection):

    property_values = get_property_values(connection)
    property_relations = get_property_relations(connection)
    cursor = connection.cursor()
    cursor.execute(items_query)
    rows = cursor.fetchall()
    results = {}
    count = 1
    for row in rows:
        row_id = row[0]
        if row_id in results.keys():
            if is_item_type(row):
                results[row_id]["type"] = row[4]
            else:
                results[row_id]["major"] = major(results[row_id]["major"],str(row[4]))


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
                row_dict["major"] = major(row_dict["major"],row[4])
            row_dict["dtype"] = row[5]
            add_properties(property_values, property_relations, row_dict)
            results[row_id] = row_dict

        results[row_id]["item_code"] = str(results[row[0]]["type"] + "_" + str(results[row[0]]["major"])).replace(" ", "_").replace("__", "_")
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