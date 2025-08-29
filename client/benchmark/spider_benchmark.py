import os
from benchmark.ai import get_sql_from_ai
from benchmark import db_config
import subprocess
import sys

bat_path = 'benchmark/spider/spider.bat'
predicted_sql_path = 'benchmark/spider/predicted.sql'

def start_workspace():
    # script_dir = os.path.dirname(os.path.abspath(__file__))[1:]
    # bat = f'python "{os.path.join(script_dir,"/spider/evaluation.py")}" --gold "{os.path.join(script_dir, "data/spider/spider_data/test_gold.sql")}" --pred predicted.sql --etype "exec" --db "{os.path.join(script_dir, "data/spider/spider_data/test_database")}" --table "{os.path.join(script_dir, "data/spider/spider_data/test_tables.json")}" > ../evaluation_results.txt 2>&1\ntype ../evaluation_results.txt'
    # with open(bat_path, "w") as f:
    #     f.write(bat)

    with open(predicted_sql_path, "w") as f:
        f.write("")
        
def append_sql(predicted_sql:str):
    with open(predicted_sql_path, "a") as f:
        f.write(predicted_sql + "\n")

def evaluate():
    # os.system(bat_path)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [
        "python", os.path.join(script_dir,"spider/evaluation.py"),
        "--gold", os.path.join(script_dir,"data/spider/spider_data/test_gold.sql"),
        "--pred", predicted_sql_path,
        "--etype", "exec",
        "--db", os.path.join(script_dir,"data/spider/spider_data/test_database"),
        "--table", os.path.join(script_dir,"data/spider/spider_data/test_tables.json"),
    ]
    with open("evaluation_results.txt", "w") as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    # sys.exit(result.returncode)

def clean_workspace():
    if os.path.exists(predicted_sql_path):
        os.remove(predicted_sql_path)
    if os.path.exists(bat_path):
        os.remove(bat_path)

def main():
    testcases = db_config.load_file(db_config.spider_testcases_path)
    start_workspace()
    #for tc in testcases:
    for i, tc in enumerate(testcases):
        if i >= 80:
            break
        db_config.set_databases([tc['db_id']])
        predicted_sql = get_sql_from_ai(tc['question'])
        if not predicted_sql.endswith(";"):
            predicted_sql += ";"
        append_sql(predicted_sql)

    evaluate()
    #clean_workspace()



