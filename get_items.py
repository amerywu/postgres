import csv





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

demographics_query = "select tce.id, tce.stem, tce.prompt, tce.dtype from testcontentelement tce where tce.id in (32089,32102,32165,32169,36823,36830 )"

options_query = "SELECT * FROM public.multiplechoiceoption"

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
    item["major"] = ""
    for pdict in prelations.values():
        if pdict["key"] == "cet_property_cati_msproperties_assessed_category_C":
            value = property_values[pdict["property_id"]]["value"]
            item["item_genre"] = value
        elif pdict["key"] == "cet_property_cati_msproperties_assessed_category_B":
            value = property_values[pdict["property_id"]]["value"]
            item["type"] = value
        elif pdict["key"] == "cet_property_cati_msproperties_assessed_category_A":
            value = property_values[pdict["property_id"]]["value"]
            item["major"] = value


def get_demographics(connection):


    cursor = connection.cursor()
    cursor.execute(demographics_query)
    rows = cursor.fetchall()
    results = {}
    count = 1
    for row in rows:
        row_id = row[0]
        row_dict = {}

        row_dict["id"] = row[0]
        row_dict["stem"] = row[1]
        row_dict["prompt"] = row[2]
        row_dict["dtype"] = row[3]


        row_dict["item_code"] = make_item_code(row_dict["dtype"], row_dict["prompt"], row_dict["id"] )
        results[row_id] = row_dict


        count = count + 1
    return results


def get_options(connection):


    cursor = connection.cursor()
    cursor.execute(options_query)
    rows = cursor.fetchall()
    results = {}
    count = 1
    for row in rows:
        row_id = row[0]
        row_dict = {}

        row_dict["id"] = row[0]
        row_dict["option"] = row[3]
        row_dict["itemid"] = row[5]
        results[row_id] = row_dict


        count = count + 1


    return results


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
        row_dict = {}

        row_dict["id"] = row[0]
        row_dict["stem"] = row[1]
        row_dict["prompt"] = row[2]


        row_dict["dtype"] = row[5]
        add_properties(property_values, property_relations, row_dict)

        row_dict["item_code"] = make_item_code(row_dict["type"], row_dict["major"], row_dict["id"] )
        results[row_id] = row_dict


        count = count + 1
    return results

def make_item_code(type,major, id):
    simple_type = type.replace("R0", "").replace("LIKERT", "L").replace("IPSATIVE", "F")
    if not major or len(major) == 0:
        major = "NA"
    if len(major) > 4:
        head = major[0:3]
        tail = major[len(major) - 2 : len(major) ]
        major = head + tail
    id = str(id)
    if len(id) > 3:
        id = id[len(id) - 3 : len(id) ]

    final_code = (simple_type+major+id).replace("_","").upper()
    return final_code

def save_csv(dict):
    with open("items.csv", "w", newline='') as f:
        w = csv.writer(f)
        thekeys = list(dict.keys())
        header = list(dict[thekeys[0]].keys())
        w.writerow(header)
        for key in thekeys:
            row = dict[key]
            w.writerow([row["id"],row["stem"],row["prompt"],row["type"],row["major"],row["dtype"]])