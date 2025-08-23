import os
from ai import get_sql_from_ai
import config
#submodule_path = Path(__file__).parent / "OpenQueryBI-UI" / "client"
#sys.path.append(str(submodule_path))

import streamlit as st
st.sidebar.title("OpenQueryBI Benchmark")

def start_workspace():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bat = f'python evaluation.py --gold "{os.path.join(script_dir, "data/spider/spider_data/test_gold.sql")}" --pred predicted.sql --etype "exec" --db "{os.path.join(script_dir, "data/spider/spider_data/test_database")}" --table "{os.path.join(script_dir, "data/spider/spider_data/test_tables.json")}" > ../evaluation_results.txt 2>&1\ntype ../evaluation_results.txt'
    with open("spider/spider.bat", "w") as f:
        f.write(bat)

    with open("spider/predicted.sql", "w") as f:
        f.write("")
        
def append_sql(predicted_sql:str):
    with open("spider/predicted.sql", "a") as f:
        f.write(predicted_sql + "\n")

def evaluate():
    os.system("spider/spider.bat")

def clean_workspace():
    if os.path.exists("spider/predicted.sql"):
        os.remove("spider/predicted.sql")
    if os.path.exists("spider/spider.bat"):
        os.remove("spider/spider.bat")

testcases = config.load_file("data/spider/spider_data/test.json")
start_workspace()
for tc in testcases:
    # TODO set databases.json env
    predicted_sql = get_sql_from_ai(tc['question'])
    if not predicted_sql.endswith(";"):
        predicted_sql += ";"
    append_sql(predicted_sql)

evaluate()
clean_workspace()



