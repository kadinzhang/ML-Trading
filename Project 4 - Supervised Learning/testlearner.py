import numpy as np
import math
import LinRegLearner as lrl
import sys

if __name__ == "__main__":
    # Open and convert .csv
    inf = open('./Data/Istanbul.csv')
    data = np.genfromtxt(inf, delimiter=',')
    # For Istanbul.csv
    data = data[1:, 1:]

    # Compute rows allocated to training and testing
    train_rows = int(0.6 * data.shape[0])

    # Training and testing data
    # Inputs (X) are worldwide index returns, output (Y) is emerging market EM return
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    print(f"{testX.shape}")
    print(f"{testY.shape}")

    # create a learner and train it  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    learner = lrl.LinRegLearner(
        verbose=True)  # create a LinRegLearner
    learner.addEvidence(trainX, trainY)  # train it

    # evaluate in sample  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    predY = learner.query(trainX)  # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print()
    print("In sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY, y=trainY)
    print(f"corr: {c[0, 1]}")

    # evaluate out of sample  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
    predY = learner.query(testX)  # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print()
    print("Out of sample results")
    print(f"RMSE: {rmse}")
    c = np.corrcoef(predY, y=testY)
    print(f"corr: {c[0, 1]}")
