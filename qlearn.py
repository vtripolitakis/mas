# Q-learning algorithm in Python

import numpy as np
import random

NUM_STATES=6
NUM_ACTIONS=6
NUM_EPISODES=5000
Alpha = 0.2
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
	q = ((1-Alpha)*Q[state,action]) + Alpha*(R[state,action] + (Gamma * getMaxQ(Q,next_state)))
	return q

def main():
	#init phase - first init Q matrix with zeros
	Q = np.zeros((NUM_STATES,NUM_ACTIONS))
	
	#define the reward function
	R = np.matrix([
		[-1 ,-1, -1, -1, 0, -1],
		[-1, -1, -1, 0, -1, 100],
		[-1, -1, -1, 0, -1, -1],
		[-1 ,0, 0, -1, 0, -1],
		[0, -1, -1, 0, -1, 100],
		[-1, 0, -1, -1, 0, 100]])

	#start episodes
	for i in range(0,NUM_EPISODES):
		#first step
		state = np.random.randint(0,NUM_STATES)
		available_actions = availableActions(R[state])
		
		while True: #do while you reach a terminal state
			action = random.choice(available_actions)
			Q[state,action]=updateRule(state,action,Q,R)
			next_state=action
			if next_state==TERMINAL_STATE:
				break
			state=next_state
			available_actions=availableActions(R[state])
	
	#done print Q matrix
	print Q

if __name__ == "__main__":
    main()