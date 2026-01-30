import pandas as pd

def analyze_csv(file):
    df = pd.read_csv(file)

    summary = {
        "total_equipment": len(df),
        "avg_flowrate": df["Flowrate"].mean(),
        "avg_pressure": df["Pressure"].mean(),
        "avg_temperature": df["Temperature"].mean(),
        "equipment_type_distribution": df["Type"].value_counts().to_dict(),
    }

    return summary
