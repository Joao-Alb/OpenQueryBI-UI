import sys
import os

DIST_N_PATH = os.path.join(os.path.dirname(__file__), "distinct_n")
if DIST_N_PATH not in sys.path:
    sys.path.insert(0, DIST_N_PATH)

# Now this works because distinct_n will be treated as top-level
from distinct_n.metrics import distinct_n_sentence_level


#from benchmark.distinct_n.distinct_n.metrics import distinct_n_sentence_level
from benchmark import db_config
from benchmark.ai import get_msgs_from_ai
import pandas as pd
from tabulate import tabulate

def evaluate(answers):
    results = {}
    sum_dist1 = 0
    sum_dist2 = 0
    for index,answer in enumerate(answers,1):
        msg = answer[-1]
        dist1 = distinct_n_sentence_level(msg.split(), 1)
        dist2 = distinct_n_sentence_level(msg.split(), 2)
        sum_dist1 += dist1
        sum_dist2 += dist2
        results[str(index)] = {
            "question": answer[0],
            "answer": msg,
            "distinct-1": dist1,
            "distinct-2": dist2,
        }
    results["average"] = {
        "distinct-1": sum_dist1 / len(answers),
        "distinct-2": sum_dist2 / len(answers),
    }
    return results

def report(results:dict):
    answers = "\n\n".join([f"Q#{k}: " + v["question"] + "\nA: " + v["answer"] for k,v in results.items() if k != "average"])
    scores = pd.DataFrame({
    key: {"distinct-1": val["distinct-1"], "distinct-2": val["distinct-2"]}
    for key, val in results.items()
    }).T
    scores.index.name = 'Question #'
    return answers+"\n###################\n" + tabulate(scores, headers='keys', tablefmt='grid')

def main():
    testcases = db_config.load_file(db_config.spider_testcases_path)
    answers = []
    for i, tc in enumerate(testcases):
        if i >= 3:
            break
        db_config.set_databases([tc['db_id']])
        answers.append((tc['question'],get_msgs_from_ai(tc['question'])))
    with open(os.path.join(os.path.dirname(__file__),"results","intratextual","evaluation_intratextual.txt"), "w", encoding="utf-8") as f:
        results = evaluate(answers)
        f.write(report(results))