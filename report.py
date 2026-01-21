import os
import pandas as pd
from datetime import datetime
def generate_report(prompt:str,responses: dict):
    os.makedirs("data/comparision", exist_ok=True)
    rows=[]
    for model,output in responses.items():
        rows.append({
            "Model":model,
            "Prompt":prompt,
            "Response":output,
            "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    df=pd.DataFrame(rows)
    df.to_csv("data/comparision/report.csv", index=False)
    return "data/comparision/report.csv"
