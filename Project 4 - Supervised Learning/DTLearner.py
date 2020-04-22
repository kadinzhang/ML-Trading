import numpy as np


class DTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        """Initialize a decision tree learner

        Args:
            leaf_size: Maximum number of samples to combine into a leaf
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.model = []

    def train(self, dataX, dataY):
        dataY = dataY[:, None]
        data = np.concatenate((dataX, dataY), axis=1)
        self.model = self.build_tree(data)

    def build_tree(self, data):
        """Build a decision tree following JR Quinlan's recursive algorithm.

        Args:
            data: concatenated X/Y data

        Returns:
            Decision tree model in NumPy array format:
                Node: [Feature index, split value, left tree, right tree]
                Leaf: ["Leaf", estimate, "NA", "NA"]
        """

        # If number of samples meets leaf size, return leaf
        if data.shape[0] <= self.leaf_size:
            return np.array([["Leaf", np.mean(data[:, -1]), "NA", "NA"]], dtype=object)
        # If all sample outputs are equal, return leaf
        if np.unique(data[:, -1]).shape[0] == 1:
            return np.array([["Leaf", data[0, -1], "NA", "NA"]], dtype=object)

        # Find feature to split on and split data between left and right trees
        feature_index = self.find_feature(data)
        split_value = np.median(data[:, feature_index])
        left_tree_data = data[data[:, feature_index] <= split_value]
        right_tree_data = data[data[:, feature_index] > split_value]

        # If split creates an empty tree, return leaf (don't want to keep creating trees)
        if left_tree_data.shape[0] == 0 or right_tree_data.shape[0] == 0:
            return np.array([["Leaf", np.mean(data[:, -1]), "NA", "NA"]])

        # Generate new left and right trees, root
        left_tree = self.build_tree(data[data[:, feature_index] <= split_value])
        right_tree = self.build_tree(data[data[:, feature_index] > split_value])
        root = np.array([[feature_index, split_value, 1, left_tree.shape[0] + 1]], dtype=object)

        return np.concatenate((root, left_tree, right_tree), axis=0)

    def find_feature(self, data):
        # Return index of feature with highest absolute correlation to outputs
        max_correlation = 0
        index = 0
        for i in range(data.shape[1] - 1):
            correlation = np.correlate(data[:, i], data[:, -1])
            if abs(correlation) > max_correlation:
                max_correlation = correlation
                index = i
        return index

    def query(self, points):
        """Estimate a set of test points given the model we built.

        Args:
            points: Numpy array with each row corresponding to a specific query.

        Returns:
            The estimated values according to the saved model.
        """
        Y = []
        for point in points:
            root = self.model[0]
            feature = root[0]
            split_value = root[1]
            next_node = 0

            while feature != "Leaf":
                if point[feature] <= split_value:
                    next_node += root[2]
                else:
                    next_node += root[3]
                root = self.model[next_node]
                feature = root[0]
                split_value = root[1]

            Y.append(root[1])
        Y = np.array(Y, dtype=float)
        return Y



