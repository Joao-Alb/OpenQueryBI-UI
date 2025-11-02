import requests

def get_plot_info(plot_id:str):
    r = requests.get(f"http://localhost:8001/plots/{plot_id}")
    return r.json()