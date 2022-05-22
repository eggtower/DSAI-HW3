import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import datetime

# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return

def getData(path1, path2):
    dateFormatter = "%Y-%m-%d %H:%M:%S"
    generation = pd.read_csv(path1, encoding='utf-8')
    consumption = pd.read_csv(path2, encoding='utf-8')
    
    h = len(generation)
    gen = np.array(generation['generation']).reshape(-1,1)
    con = np.array(consumption['consumption']).reshape(-1,1)
    last_date = datetime.datetime.strptime(generation["time"][h-1], dateFormatter)

    gScalar = MinMaxScaler()
    cScalar = MinMaxScaler()
    
    gen = gScalar.fit_transform(gen)
    con = cScalar.fit_transform(con)
    
    gen = gen[-72:].reshape(-1,1,72)
    con = con[-72:].reshape(-1,1,72)
    
    return gen[-72:], gScalar, con[-72:], cScalar, last_date

def test_model(gen, con):
    genModel = tf.keras.models.load_model('generationModel_v1.h5')
    pdGen = genModel.predict(gen)
    conModel = tf.keras.models.load_model('consumptionModel_v1.h5')
    pdCon = conModel.predict(con)
    return pdGen.reshape(-1, 1), pdCon.reshape(-1, 1)

def rule(pdGen, pdCon, last_date):

    ans = []
    for i in range(0, len(pdGen)):
        last_date = last_date + datetime.timedelta(hours=1)
        gap = pdCon[i] - pdGen[i]
        if (gap > 0):
            for j in range(int(gap)):
                ans.append([str(last_date), "buy", 2.3, 1])
        elif (gap < 0):
            ans.append([str(last_date), "sell", 1.5, 1])
    return ans


if __name__ == "__main__":
    args = config()

    gen, gScalar, con, cScalar, last_date = getData(config().generation, config().consumption)
    pdGen, pdCon = test_model(gen, con)
    
    pdGen = gScalar.inverse_transform(pdGen)
    pdCon = cScalar.inverse_transform(pdCon)
    
    data = rule(pdGen, pdCon, last_date)
    
    output(args.output, data)
