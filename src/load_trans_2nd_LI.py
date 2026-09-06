import pandas as pd

#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\PSFB\trans_2nd_LI.csv"

def load_trans_2nd_LI(csv_path):
    df=pd.read_csv(csv_path)
#    trans_2nd_LI=df[["2ndary current A","L2 uH"]].to_numpy()       #interpolate.pyでのバグを受けてこちらを下の行に変更
    trans_2nd_LI=df[["2ndary current A","L2 uH"]]
    return trans_2nd_LI

#trans_2nd_LI=load_trans_2nd_LI(csv_path)
#print(trans_2nd_LI)