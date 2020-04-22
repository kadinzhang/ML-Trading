import numpy as np


class BagLearner(object):

    def __init__(self, learner, kwargs={}, bags=10, boost=False, verbose=False):
        """Initiate a bootstrap aggregating learner.

        Args:
            learner: Learner object to use
            kwargs: Learner-specific arguments, ex. {"leaf_size": 1}
            bags: Number of bags to create
            boost: Whether to implement boosting
        """

        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []

    def train(self, dataX, dataY):
        # Merge data
        dataY = dataY[:, None]
        data = np.hstack((dataX, dataY))

        # Create learner instances
        for i in range(self.bags):
            self.learners.append(self.learner(**self.kwargs))

        # Train each learner with a random sample of 60% training data
        sample_size = data.shape[0]
        bag_size = int(0.6 * data.shape[0])
        for learner in self.learners:
            bag_indices = np.random.choice(sample_size, bag_size, replace=False)
            bag_data = data[bag_indices]
            learner.train(bag_data[:, :-1], bag_data[:, -1])

    def query(self, points):
        """Estimate a set of test points across each learner and combine results.

        Args:
            points: Numpy array with each row corresponding to a specific query.

        Returns:
            The estimated values according to the bag learner.
        """

        estimates = np.empty((points.shape[0], 0), int)
        for learner in self.learners:
            predY = learner.query(points)
            estimates = np.hstack((estimates, predY[:, None]))
        return np.mean(estimates, axis=1)










