import pandas as pd

def fLoadData():
    MotivationFileKey = pd.read_csv(r'Data/MotivationImages.csv')

    return MotivationFileKey
