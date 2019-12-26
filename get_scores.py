def get_property_values(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.contentelementtypeproperty limit 1000")
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


def get_scores(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.testcontentelementscore order by id limit 1000")
    rows = cursor.fetchall()
    all_scores_dict = {}

    for row in rows:
        testid = row[9]
        if testid in all_scores_dict.keys():
            test_dict = all_scores_dict[testid]
        else:
            test_dict = {}
            all_scores_dict[testid] = test_dict

        row_dict = {}
        row_dict["scoreid"] = row[0]
        row_dict["testtype"] = row[3]
        row_dict["testid"] = row[9]
        row_dict["created"] = row[2]
        row_dict["itemid"] = row[5]
        row_dict["score"] = row[4]
        test_dict[row[0]] = row_dict

    return all_scores_dict


def get_responses(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.testcontentelementresponse order by id limit 4000")
    rows = cursor.fetchall()
    all_responses_dict = {}

    for row in rows:
        testid = row[15]
        if testid in all_responses_dict.keys():
            test_dict = all_responses_dict[testid]
        else:
            test_dict = {}
            all_responses_dict[testid] = test_dict

        row_dict = {}
        row_dict["responseid"] = row[0]
        row_dict["durationinseconds"] = row[2]
        row_dict["poolid"] = row[5]
        row_dict["shortresponse"] = row[6]
        row_dict["testid"] = row[15]
        row_dict["itemid"] = row[12]
        row_dict["scoreid"] = row[13]
        test_dict[row[13]] = row_dict

    return all_responses_dict



def get_response_attributes(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.responseattribute ORDER BY id limit 4000")
    rows = cursor.fetchall()
    all_attributes_dict = {}

    for row in rows:
        responseid = row[5]
        if responseid in all_attributes_dict.keys():
            attribute_dict = all_attributes_dict[responseid]
        else:
            attribute_dict = {}
            all_attributes_dict[responseid] = attribute_dict

        row_dict = {}
        row_dict["attributeid"] = row[0]
        row_dict["attributetype"] = row[1]
        row_dict["attributevalue"] = row[4]
        row_dict["responseid"] = row[5]

        attribute_dict[row[0]] = row_dict



    return all_attributes_dict

def _win_lose_attribute(response_id, attributes_dict):
    attrs = attributes_dict[response_id]
    for attr in attrs.values():
        if attr["attributetype"] == "BEAT_OUT":
            attribute =  attr["attributevalue"]
        elif attr["attributetype"] =="LOST TO":
            attribute = attr["attributevalue"]
        else:
            attribute = ""
    return attribute


