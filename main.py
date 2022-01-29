import requests
import json
import pprint
import psycopg2
from psycopg2.extras import execute_values

per_state_year = {}

state_level_data = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "DC",
    "FL",
    "GA",
    "GU",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "MP",
    "OH",
    "OK",
    "OR",
    "PA",
    "PR",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "VI",
    "WA",
    "WV",
    "WI",
    "WY",
]

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
    total_grads_wages_json = requests.get('https://datausa.io/api/data?measure=ygcpop%20RCA,Total%20Population,Total%20Population%20MOE%20Appx,Average%20Wage,Average%20Wage%20Appx%20MOE,Record%20Count&drilldowns=PUMA&Record%20Count%3E=5')
    total_grads_wages_engineers_json = requests.get('https://datausa.io/api/data?CIP2=14&measure=ygcpop%20RCA,Total%20Population,Total%20Population%20MOE%20Appx,Average%20Wage,Average%20Wage%20Appx%20MOE,Record%20Count&drilldowns=PUMA&Record%20Count%3E=5&Workforce%20Status=true')

    if total_grads_json.status_code == 200 and total_grads_engineers_json.status_code == 200:
        extract_graduations(total_grads_json.json()['data'])
        extract_graduations_engineers(total_grads_engineers_json.json()['data'])

    if total_grads_wages_json.status_code == 200 and total_grads_wages_engineers_json.status_code == 200:
        extract_graduations_wages(total_grads_wages_json.json()['data'])
        extract_graduations_wages_engineers(total_grads_wages_engineers_json.json()['data'])

    find_percentages(7,6,5)
    cur, conn = connect_db()
    

    listthin = []
    for x in per_state_year.values():
        vals = tuple(x)
        listthin.append(vals)

    cur.executemany("INSERT into summersalt.state_data (state,year,total_grads,total_grads_engineer,percentage_grads_engineer,total_wage_estimate,total_wage_estimate_engineer,percentage_wage_engineer) VALUES (%s,%s,%s,%s,%s, %s,%s,%s)",listthin)
    conn.commit()
    conn.close()


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
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], record["Completions"], 0, "", 0.0, 0.0, ""]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid")

def extract_graduations_engineers(json_obj):
    for record in json_obj:
        #print(record["PUMA"][-2:].upper() in state_level_data)
        #print(type(record["PUMA"][-2:].upper()))
        if record["PUMA"][-2:].upper() in state_level_data:
            if str(record["Year"] + record["PUMA"][-2:]).lower() in per_state_year:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][3] = per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][3] + record["Completions"]
            else:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], 0, record["Completions"], "", 0.0, 0.0, ""]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid")

def extract_graduations_wages(json_obj):
    for record in json_obj:
        if "79500US" in record["PUMA"]: #with more time this can be cleaned up.
            record["PUMA"] = record["PUMA"][:-17]
        if record["PUMA"][-2:].upper() in state_level_data:
            if str(record["Year"] + record["PUMA"][-2:]).lower() in per_state_year:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][5] = per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][5] + record["Average Wage"]
            else:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], 0, 0, "", record["Average Wage"], 0.0, ""]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid: wage")

def extract_graduations_wages_engineers(json_obj):
    for record in json_obj:
        if "79500US" in record["PUMA"]: #with more time this can be cleaned up.
            record["PUMA"] = record["PUMA"][:-17]
        if record["PUMA"][-2:].upper() in state_level_data:
            if str(record["Year"] + record["PUMA"][-2:]).lower() in per_state_year:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][6] = per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()][6] + record["Average Wage"]
            else:
                per_state_year[str(record["Year"] + record["PUMA"][-2:]).lower()] = [record["PUMA"][-2:], record["Year"], 0, 0, "", 0.0, record["Average Wage"], ""]
        elif record["PUMA"] == "#null":
            pass
            #no state was provided
        else:
            print("State not Valid: wage E")

def find_percentages(result, numerator, denomiator):
    for value in per_state_year.values():
        value[4] = str(round((value[3] / value[2]), 3) * 100)
        if value[6] != 0.0:
            value[7] = str((value[6] / value[5]) * 100)
        else:
            value[7] == "0"


main()