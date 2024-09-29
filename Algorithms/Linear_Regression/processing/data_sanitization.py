import pandas as pd 
import csv

def is_CSV(file_path):
    if not file_path.lower().endswith('.csv'):
        return False
    try:
        with open(file_path, newline='') as file:
            csv.reader(file)
            return True
    except Exception:
        print(f"Error Reading File: {Exception}")
        return False                
    
def reading_file(file_path):
    if(is_CSV(file_path)):
        dataframe = pd.read_csv(file_path, delimiter=',')
        return dataframe
    else:
        print(f"The Given File Is Not A CSV File")