import json
from difflib import get_close_matches
import sys

data = json.load(open('data/data.json'))

## If a word has multiple definitions, we need to format it so that there is one 'tidy' response per line.
## Note that the process is different for interactive versus non-interactive python sessions.
def format_definition(definition_list):
    out_definition = str(definition_list)
    if bool(getattr(sys, 'ps1', sys.flags.interactive)):
        list_sep = "', '"
        str_idx_start = out_definition.find('u')+2
    else:
        list_sep = "', u'"
        if type(definition_list) == list:
            str_idx_start = 2
        else:
            str_idx_start = 1
    out_definition = out_definition.replace(list_sep, "\n")
    out_definition = out_definition[str_idx_start:len(out_definition)-2]
    return(out_definition)

## Does the response begin with the letter 'y' (e.g. for 'Yes' or 'Yep' or 'Yeah man')?
def format_response(response):
    if response.lower()[0] == 'y':
        return(True)
    else:
        return(False)

def query_definition(data_json, key):
    if key in data_json.keys():
        definition = format_definition(data_json[key.lower()])
        return(definition)
    elif len(get_close_matches(key, data_json.keys())) > 0:
        if bool(getattr(sys, 'ps1', sys.flags.interactive)):
            resp = input("Did you mean %s?:" % get_close_matches(key, data_json.keys())[0])
        else:
            resp = 'Y'
        if format_response(resp):
            definition = format_definition(data_json[get_close_matches(key, data_json.keys())[0]])
            return(definition)
    else:
        return('No definition is available for the word.')

## Print the outputs of the functions from any arbitrary word. Voila.
print(query_definition(data, 'rain'))
