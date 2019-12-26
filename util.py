


def print_row_value(row, dict, keylist):
    return_string = ""
    for key in keylist:
        return_string += str(row[dict[key]]) + ","
    return return_string

def item_or_empty(adict, key):
    if key in adict.keys():
        return adict[key]
    else:
        return ""