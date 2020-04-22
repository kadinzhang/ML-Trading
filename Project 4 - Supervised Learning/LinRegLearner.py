import numpy as np


class LinRegLearner(object):

    def __init__(self, verbose=False):
        pass

    def train(self, dataX, dataY):
        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:, 0:dataX.shape[1]] = dataX

        # build and save the model  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY, rcond=None)

    def query(self, points):
        """Estimate a set of test points given the model we built.

        Args:
            points: Numpy array with each row corresponding to a specific query.

        Returns:
            The estimated values according to the saved model.
        """
        return (self.model_coefs[:-1] * points).sum(axis=1) + self.model_coefs[-1]