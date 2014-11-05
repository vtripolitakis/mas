# Q-learning algorithm in Python

import numpy as np
import scipy as sp
import random

NUM_STATES=6
NUM_ACTIONS=6
NUM_EPISODES=5000
Gamma = 0.8
TERMINAL_STATE=5


#returns available actions for the current state
def availableActions(state):
	available_actions=[]
	for i in range(0,NUM_ACTIONS):
		if ((state[0,i]>=0)):
			available_actions.append(i)
	return available_actions

def getMaxQ(Q,next_state):
	return np.max(Q[next_state])

def updateRule(state,action,Q,R):
	next_state=action
	q = R[state,action] + (Gamma * getMaxQ(Q,next_state))
	return q


#init phase
Q = np.zeros((NUM_STATES,NUM_ACTIONS))
R = np.matrix([[-1 ,-1, -1, -1, 0, -1],[-1, -1, -1, 0, -1, 100],[-1, -1, -1, 0, -1, -1],[-1 ,0, 0, -1, 0, -1],[0, -1, -1, 0, -1, 100],[-1, 0, -1, -1, 0, 100]])


for i in range(0,NUM_EPISODES):
	#first step
	state = np.random.randint(0,NUM_STATES)
	available_actions = availableActions(R[state])
	
	while True:
		action = random.choice(available_actions)
		Q[state,action]=updateRule(state,action,Q,R)
		next_state=action
		if next_state==TERMINAL_STATE:
			break
		state=next_state
		available_actions=availableActions(R[state])	
		

print Q