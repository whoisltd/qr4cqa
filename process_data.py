import os
import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    df = pd.read_csv('data/Address.csv')
    df['CustomerAddress'] = df['CustomerAddress'].str.lower()
    print('max source length', df["CustomerAddress"].str.len().max())
    df['areaFull'] = df['areaFull'].str.lower()
    print('max target length', df["areaFull"].str.len().max())
    train, test = train_test_split(df, test_size=0.2, stratify=df['provName'], random_state=42)
    train.to_csv('data/train_v1.csv', index=False)
    test.to_csv('data/test_v1.csv', index=False)