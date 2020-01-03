import torch
from all.nn import weighted_mse_loss
from ._agent import Agent


class DDQN(Agent):
    '''
    Double Deep Q-Network

    In additional to the introduction of "double" Q-learning,
    this agent also supports prioritized experience replay
    if replay_buffer is a prioritized buffer.
    '''
    def __init__(self,
                 q,
                 policy,
                 replay_buffer,
                 loss=weighted_mse_loss,
                 discount_factor=0.99,
                 minibatch_size=32,
                 replay_start_size=5000,
                 update_frequency=1,
                 ):
        # objects
        self.q = q
        self.policy = policy
        self.replay_buffer = replay_buffer
        self.loss = staticmethod(loss)
        # hyperparameters
        self.replay_start_size = replay_start_size
        self.update_frequency = update_frequency
        self.minibatch_size = minibatch_size
        self.discount_factor = discount_factor
        # data
        self.env = None
        self.state = None
        self.action = None
        self.frames_seen = 0

    def act(self, state, reward):
        self._store_transition(state, reward)
        self._train()
        self.state = state
        self.action = self.policy(state)
        return self.action

    def _store_transition(self, state, reward):
        if self.state and not self.state.done:
            self.frames_seen += 1
            self.replay_buffer.store(self.state, self.action, reward, state)

    def _train(self):
        if self._should_train():
            (states, actions, rewards, next_states, weights) = self.replay_buffer.sample(
                self.minibatch_size)

            # update q-network
            values = self.q(states, actions)
            next_actions = torch.argmax(self.q.eval(next_states), dim=1)
            targets = rewards + self.discount_factor * self.q.target(next_states, next_actions)
            self.q.reinforce(self.loss(values, targets, weights))

            # update replay buffer
            td_errors = targets - values
            self.replay_buffer.update_priorities(td_errors.abs())

    def _should_train(self):
        return (self.frames_seen > self.replay_start_size and
                self.frames_seen % self.update_frequency == 0)
