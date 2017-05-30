from PyPi.algorithms.agent import Agent
from PyPi.utils.dataset import max_QA, parse_dataset


class BatchTD(Agent):
    """
    Implements functions to run Batch algorithms.
    """
    def __init__(self, agent, mdp, **params):
        super(BatchTD, self).__init__(agent, mdp, **params)

    def updates(self):
        pass

    def __str__(self):
        return self.__name__


class FQI(BatchTD):
    """
    Fitted Q-Iteration algorithm.
    "Tree-Based Batch Mode Reinforcement Learning", Ernst D. et.al.. 2005.
    """
    def __init__(self, agent, mdp, **params):
        self.__name__ = 'FQI'

        super(FQI, self).__init__(agent, mdp, **params)

    def fit(self, dataset, n_iterations):
        """
        Fit loop.

        # Arguments
            n_iterations (int > 0): number of iterations
        """
        target = None
        for i in range(n_iterations):
            self.logger.info('Iteration: %d' % (i + 1))
            target = self.partial_fit(dataset, target,
                                      **self.params['fit_params'])

    def partial_fit(self, x, y, **fit_params):
        """
        Single fit iteration.

        # Arguments
            x (np.array): input dataset.
            y (np.array): target.
        """
        state, action, reward, next_states, absorbing, last =\
            parse_dataset(x, self.mdp_info['observation_space'].dim,
                          self.mdp_info['action_space'].dim)
        if y is None:
            y = reward
        else:
            maxq, _ = max_QA(next_states, absorbing, self.approximator,
                             self.policy.discrete_actions)
            y = reward + self.mdp_info['gamma'] * maxq

        sa = (state, action)
        self.approximator.fit(sa, y, **fit_params)

        return y


class DoubleFQI(FQI):
    """
    Double Fitted Q-Iteration algorithm.
    "Estimating the Maximum Expected Value in Continuous Reinforcement Learning
    Problems". D'Eramo C. et. al.. 2017.
    """
    def __init__(self, agent, mdp, **params):
        self.__name__ = 'DoubleFQI'

        super(DoubleFQI, self).__init__(agent, mdp, **params)

    def partial_fit(self, x, y, **fit_params):
        pass


class WeightedFQI(FQI):
    """
    Weighted Fitted Q-Iteration algorithm.
    "Estimating the Maximum Expected Value in Continuous Reinforcement Learning
    Problems". D'Eramo C. et. al.. 2017.
    """
    def __init__(self, agent, mdp, **params):
        self.__name__ = 'WeightedFQI'

        super(WeightedFQI, self).__init__(agent, mdp, **params)

    def partial_fit(self, x, y, **fit_params):
        pass