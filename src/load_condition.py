import pandas as pd

def load_condition(csv_path):
    df=pd.read_csv(csv_path)
    n1=df["turn 1"].iloc[0].astype('int')
    n2=df["turn 2"].iloc[0].astype('int')
    v1=float(df["V1 V"].iloc[0])
    v2=float(df["V2 V"].iloc[0])
    i2=float(df["I2 A"].iloc[0])
    fs=float(df["fs kHz"].iloc[0])*1000
    duty=v2/v1*n1/n2
    tcyc=1/fs
    ton=tcyc/2*duty
    toff=tcyc/2-ton

    return {
        "n1":n1,
        "n2":n2,
        "v1":v1,
        "v2":v2,
        "i2":i2,
        "fs":fs,
        "duty":duty,
        "tcyc":tcyc,
        "ton":ton,
        "toff":toff
        }




