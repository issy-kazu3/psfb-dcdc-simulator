import pandas as pd

#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\PSFB\choke_LI.csv"

def load_choke_LI(csv_path):
    df=pd.read_csv(csv_path)
#    choke_LI=df[["A","uH"]].to_numpy() #interpolate.pyでのバグを受けてこちらを下の行に変更
    choke_LI=df[["A","uH"]]
    return choke_LI

#choke_LI=load_choke_LI(csv_path)
#print(choke_LI)
