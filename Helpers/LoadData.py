import pandas as pd
import os

def fLoadData():
    file_dir = os.path.dirname(__file__)
    csv_path = os.path.join(file_dir, "..", "Data", "MotivationImages.csv")
    MotivationFileKey = pd.read_csv(csv_path)

    return MotivationFileKey
