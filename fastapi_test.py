# /opt/anaconda3/bin/python3
import requests
import pandas as pd
from pathlib import Path
# from src.config import DATA_DIR

def main():
    # data_path: Path = DATA_DIR / "raw" / "WineQT.csv"

    # df = pd.read_csv(data_path)

    df = pd.read_csv("/Users/chinmairaman/Documents/Classes/Hariom Jha/python_project/data/raw/WineQT.csv")

    for i in range(10):

        # Get ith row
        row = df.iloc[i]

        base_url = "http://54.183.60.217:8000"
        endpoint = f"{base_url}/create_item/"
        params = {
            "fixed_acidity": str(row["fixed acidity"]),
            "volatile_acidity": str(row["volatile acidity"]),
            "citric_acid": str(row["citric acid"]),
            "residual_sugar": str(row["residual sugar"]),
            "chlorides": str(row["chlorides"]),
            "free_sulfur_dioxide": str(row["free sulfur dioxide"]),
            "total_sulfur_dioxide": str(row["total sulfur dioxide"]),
            "density": str(row["density"]),
            "pH": str(row["pH"]),
            "sulphates": str(row["sulphates"]),
            "alcohol": str(row["alcohol"])
        }

        # params = {
        #     "fixed_acidity": "7.4",
        #     "volatile_acidity": "0.7",
        #     "citric_acid": "0.0",
        #     "residual_sugar": "1.9",
        #     "chlorides": "0.076",
        #     "free_sulfur_dioxide": "11.0",
        #     "total_sulfur_dioxide": "34.0",
        #     "density": "0.9978",
        #     "pH": "3.51",
        #     "sulphates": "0.56",
        #     "alcohol": "9.4"
        # }
        response = requests.post(endpoint, params=params)
        # print(response.json())

        # Get actual quality
        actual_quality = row["quality"]
        print(f"Actual quality: {actual_quality}, Predicted quality: {response.json().get('prediction')}")
        print(actual_quality == response.json().get("prediction"))

# if __name__ == "__main__":
#     main()