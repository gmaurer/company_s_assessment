import requests
import json
import pprint
import psycopg2
from psycopg2.extras import execute_values

per_state_year = {}

state_level_data = {
    "AL": [],
    "AK": [],
    "AZ": [],
    "AR": [],
    "CA": [],
    "CO": [],
    "CT": [],
    "DE": [],
    "DC": [],
    "FL": [],
    "GA": [],
    "GU": [],
    "HI": [],
    "ID": [],
    "IL": [],
    "IN": [],
    "IA": [],
    "KS": [],
    "KY": [],
    "LA": [],
    "ME": [],
    "MD": [],
    "MA": [],
    "MI": [],
    "MN": [],
    "MS": [],
    "MO": [],
    "MT": [],
    "NE": [],
    "NV": [],
    "NH": [],
    "NJ": [],
    "NM": [],
    "NY": [],
    "NC": [],
    "ND": [],
    "MP": [],
    "OH": [],
    "OK": [],
    "OR": [],
    "PA": [],
    "PR": [],
    "RI": [],
    "SC": [],
    "SD": [],
    "TN": [],
    "TX": [],
    "UT": [],
    "VT": [],
    "VA": [],
    "VI": [],
    "WA": [],
    "WV": [],
    "WI": [],
    "WY": []
}

class Record:
    def __init__(self,state,year,total_grads,total_grads_engineer,percentage_grads_engineer,total_wage_estimate,total_wage_estimate_engineer,percentage_wage_engineer):
        self.state = state
        self.year = year
        self.total_grads = total_grads
        self.total_grads_engineer = total_grads_engineer
        self.percentage_grads_engineer = percentage_grads_engineer
        self.total_wage_estimate = total_wage_estimate
        self.total_wage_estimate_engineer = total_wage_estimate_engineer
        self.percentage_wage_engineer = percentage_wage_engineer

def main():
    

    total_grads_json = requests.get('https://datausa.io/api/data?measures=Completions&drilldowns=PUMA,University')
    total_grads_engineers_json = requests.get('https://datausa.io/api/data?CIP=14&drilldowns=PUMA&measure=Completions')
    #pprint.pprint(total_grads_json.json()['data'][0])
    #pprint.pprint(total_grads_engineers_json.json()['data'][0])

    if total_grads_json.status_code == 200 and total_grads_engineers_json.status_code == 200:
        extract_graduations(total_grads_json.json()['data'])
        extract_graduations_engineers(total_grads_engineers_json.json()['data'])

        find_percentages()

    cur, conn = connect_db()
    

    listthin = []
    for x in per_state_year.values():
        vals = tuple(x)
        listthin.append(vals)

    cur.executemany("INSERT into summersalt.state_data (state,year,total_grads,total_grads_engineer,percentage_grads_engineer,total_wage_estimate,total_wage_estimate_engineer,percentage_wage_engineer) VALUES (%s,%s,%s,%s,%s, %s,%s,%s)",listthin)
    conn.commit()
    cur.close()


def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="summersalt_db",
        user="postgres",
        password="darling")

    cur = conn.cursor()
    return cur, conn    

    ''' 
    Requests given for assessment:
    https://datausa.io/api/data?measures=Completions&drilldowns=PUMA,University
    https://datausa.io/api/data?CIP=14&drilldowns=PUMA&measure=Completions
    https://datausa.io/api/data?measure=ygcpop%20RCA,Total%20Population,Total%20Population%20
    https://datausa.io/api/data?CIP2=14&measure=ygcpop%20RCA,Total%20Population,Total%20Popul

    '''

def extract_graduations(json_obj):
    for record in json_obj:
        if record["PUMA"][-2:].upper() in state_level_data:
            if str(record["Year"] + record["PUMA"][-2:]).lower() in per_state_year:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][2] = per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][2] + record["Completions"]
            else:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], record["Completions"], 0, "", 0.0, 0.0, "test"]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid")

def extract_graduations_engineers(json_obj):
    for record in json_obj:
        if record["PUMA"][-2:].upper() in state_level_data:
            if str(record["Year"] + record["PUMA"][-2:]).lower() in per_state_year:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][3] = per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][3] + record["Completions"]
            else:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], 0, record["Completions"], "", 0.0, 0.0, "tests"]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid")

def find_percentages():
    for value in per_state_year.values():
        value[4] = str(round((value[3] / value[2]), 3) * 100)


main()