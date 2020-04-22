import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import sys

if __name__ == "__main__":
    inf = open('./Data/Istanbul.csv')
    # inf = open('./Data/winequality-red.csv')
    data = np.genfromtxt(inf, delimiter=',')

    # Istanbul
    data = data[1:, 1:]
    data = data[:10, :]

    # Compute rows allocated to training and testing
    train_rows = int(0.6 * data.shape[0])

    # Training and testing data
    # Inputs (X) are worldwide index returns, output (Y) is emerging market EM return
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    # print(f"{testX.shape}")
    # print(f"{testY.shape}")

    # ____________________Learners______________________
    # learner = lrl.LinRegLearner(
    #     verbose=True)
    # learner = rtl.RTLearner()
    learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": 1}, bags=10, boost=False, verbose=False)
    # learner = dtl.DTLearner()
    learner.train(trainX, trainY)  # train it

    predY = learner.query(trainX)
    # predY = predY[:, None]
    # trainY = trainY[:, None]


    # Calculate statistics
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print("In sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY.T, trainY.T)
    print(f"corr: {c[0, 1]}")

    # evaluate out of sample
    predY = learner.query(testX)
    # predY.round(decimals=3)
    np.set_printoptions(precision=2)

    rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print()
    print("Out of sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY.T, testY.T)
    print(f"corr: {c[0, 1]}")
