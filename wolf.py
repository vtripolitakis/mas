# Win or Lose Fast (WoLF) Policy hill Climbing algorithm in Python
# As described in "Rational and Convergent Learning in Stochastic Games" by Bowling and Veloso

import numpy as np
import random

NUM_STATES=6
NUM_ACTIONS=6
NUM_EPISODES=3000
Alpha = 0.2
Gamma = 0.8
Delta_win = 0.001
Delta_lose = 0.003
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

def selectAction(state,Policy):	 	
	p1=Policy[state,:]	
	#does it sum to 1?
	if (np.sum(p1)==1.0):		
		return np.random.choice(6,1,p=p1)
	else:
		p1 /= p1.sum()	
		return np.random.choice(6,1,p=p1)

def calculateDelta(state,Q,Policy,MeanPolicy,Delta_win,Delta_lose):
	sumPolicy=0.0
	sumMeanPolicy=0.0		
	for i in range(0,NUM_ACTIONS):
		sumPolicy=sumPolicy+(Policy[state,i]*Q[state,i])
		sumMeanPolicy=sumMeanPolicy+(MeanPolicy[state,i]*Q[state,i])
	if (sumPolicy>sumMeanPolicy):
		return Delta_win
	else:
		return Delta_lose			

def policyUpdate(state,Policy,MeanPolicy,Q,Delta_win,Delta_lose):
	maxQValueIndex = np.argmax(Q[state])
	for i in range(0,NUM_ACTIONS):
		Delta_plus = calculateDelta(state,Q,Policy,MeanPolicy,Delta_win,Delta_lose)
		Delta_minus = ((-1.0)*Delta_plus)/((NUM_ACTIONS*1.0) - 1.0)
		print Delta_plus
		if (i==maxQValueIndex):
			Policy[state,i] = min(1.0,Policy[state,i] + Delta_plus)
		else:
			#TODO: edw 8elei prosoxh kanonika to delta minus 8a prepei na einai me ton ari8mo twn non zero elements - alliws xalaei to normalization
			Policy[state,i] = max(0.0,Policy[state,i] + Delta_minus)
	return Policy

def meanPolicyUpdate(state,C,MeanPolicy,Policy):
	#print C
	#print Policy[state,:]
	#print MeanPolicy[state,:]
	for i in range(0,NUM_ACTIONS):
		MeanPolicy[state,i] = MeanPolicy[state,i] + ((1.0/C[state]) * (Policy[state,i]-MeanPolicy[state,i]))		
	#print MeanPolicy[state,:]	
	return	MeanPolicy

def main():
	#init phase - first init Q matrix with zeros
	Q = np.zeros((NUM_STATES,NUM_ACTIONS))
	#init phase - second: initialize C matrix with zeros
	C = np.zeros(NUM_STATES)
	#init phase - third: init Policy matrix with equal values 1/(NUM_ACTIONS)
	Policy = np.empty([NUM_STATES,NUM_ACTIONS])
	#init phase - fourth: init MeanPolicy with zeros
	MeanPolicy = np.zeros((NUM_STATES,NUM_ACTIONS))

	#TODO: edw 8elei na kanw automata to array auto.
	Policy = np.array([
		[0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
		[0.0, 0.0, 0.0, 1.0/2, 0.0, 1.0/2],
		[0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
		[0.0 ,1.0/3, 1.0/3, 0.0, 1.0/3, 0.0],
		[1.0/3, 0.0, 0.0, 1.0/3, 0.0, 1.0/3],
		[0.0, 1.0/3, 0.0, 0.0, 1.0/3, 1.0/3]])
	
	#define the reward function
	# -1 means not available and is ignored
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
			#select random state from the Policy table - no exploration for the moment - add an if with epsilon-greedy exploration
			#problhma - edw ti ginetai me ta non-available actions - kanonika prpeei na ginei init o pinakas alliws me diaforetiko Policy ana state
			#action = random.choice(available_actions) 
			
			if (isinstance (state, (np.ndarray,np.generic))):
				action = selectAction(state[0],Policy)
			else:
				action = selectAction(state,Policy)			
			
			Q[state,action]=updateRule(state,action,Q,R)

			#edw arxizei o kwdikas tou WoLF-PHC
			C[state] = C[state]+1
			MeanPolicy = meanPolicyUpdate(state,C,MeanPolicy,Policy)
			#edw kanoume twra update to Policy matrix
			Policy = policyUpdate(state,Policy,MeanPolicy,Q,Delta_win,Delta_lose)

			#debug
			
			#raw_input('press enter')
			#end debug

			next_state=action
			if next_state==TERMINAL_STATE:
				break
			state=next_state
			available_actions=availableActions(R[state])

	#done print Q matrix
	print Q
	print Policy
	print C
	print np.sum(C)
	print MeanPolicy

if __name__ == "__main__":
    main()