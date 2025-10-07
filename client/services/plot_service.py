import requests

def get_plot_info(plot_id:str):
    r = requests.get(f"https://openquerybi.online/plots/{plot_id}")
    return r.json()