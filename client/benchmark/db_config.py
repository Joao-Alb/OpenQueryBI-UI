import json
import os
import requests

spider_databases_path = 'benchmark/data/spider/spider_data/test_tables.json'
spider_testcases_path = 'benchmark/data/spider/spider_data/test.json'

def load_file(databases_path):
    with open(databases_path, 'r') as file:
        databases = json.load(file)
    return databases

def save_mcp_databases(databases:list):
    body = databases
    r = requests.post("http://openquerybi:8001/set_databases_configs/", json=body)
    #export result of requests to a file for debugging
    with open("benchmark/db_config_log.txt", "w") as f:
        f.write(f"Request body 4: {json.dumps(body, indent=2)}\n")
        f.write(f"Response status code: {r.status_code}\n")
        f.write(f"Response body: {r.text}\n")

def set_databases(databases_ids:list[str]):
    spider = load_file(spider_databases_path)
    mcp = {"databases":[]}
    for id in databases_ids:
        for db in spider:
            if db['db_id'] == id:
                mcp['databases'].append({
                    "name": id,
                    "config":{
                        "dialect":"sqlite",
                        "username":"",
                        "password":"",
                        "host":"",
                        "port":"",
                        "database":os.path.abspath(f"test/test_database/{id}/{id}.sqlite")
                    },
                    "tables":db['table_names'],
                    "type": "sqlite"
                })
    save_mcp_databases(mcp["databases"])