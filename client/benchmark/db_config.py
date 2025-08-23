import json
import os

mcp_databases_path = 'OpenQueryBI\\servers\\OpenQueryBI\\databases.json'
spider_databases_path = 'data\\spider\\spider_data\\test_tables.json'

def load_file(databases_path):
    with open(databases_path, 'r') as file:
        databases = json.load(file)
    return databases

def save_mcp_databases(databases, databases_path=mcp_databases_path):
    with open(databases_path, 'w') as file:
        json.dump(databases, file, indent=4)

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
                        "database":os.path.abspath(f"data\\spider\\spider_data\\test_database\\{id}\\{id}.sqlite")
                    },
                    "tables":db['table_names'],
                    "type": "sqlite"
                })
    save_mcp_databases(mcp)