import seaborn as sns
import matplotlib.pyplot as plt
from collections import deque
import random
import numpy as np

# This clas generates neuron objects which are embedded in the brain matrix
class Neurons:
    def __init__(self, row, column):
        self.id =f"Neuron-{row}-{column}"
        self.threshold = random.randint(1,10)
        self.fired = False
        self.last_update_time = 0
        self.last_signal_id = 0

# This code block initializes the Brain class
# The Brain class creates the brain structure in a matrix format
# Where each entry is a neuron object.
class Brain:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns

        # Creates the barin matrix which contains the neurons
        self.matrix = [[Neurons(r,c) for c in range(self.cols)] for r in range(self.rows)] 

        # Creates a 2D aray that stores the current energy state of each neuron which will
        # be used to determine the rest period and how much energy would increase for each neuron
        self.energymatrix = np.full((self.rows,self.cols), 100) 

        # This 3D matrix stores the weights for the connections as random numbers
        # The 3D dimension contains 4 random float numbers which will determine the strength
        # Of the connection in each direction
        self.cweights = np.random.uniform(0.1,1.0,(self.rows,self.cols,4))

        # Tells when was was each neuron last updated, if a neuron has never fired
        # this will remain zero because it was never updated
        self.last_update_map = np.zeros((self.rows, self.cols))

        # Starts at 0 neurons fired
        self.current_time = 0

        # Stores how many times the class Brain has been initialized
        self.event_id = 0
        
    # The connections method defines the connections that exist between neurons
    # r,c are the Neuron's row, column indexes to find the connections for
    def connections(self,r,c):

        # Guide: up(r-1,c,0), right(r,c+1,1), down(r+1,c,2), left(r,c-1,3)
        # These are the possible connection indexes 

        valid_connections = []
        if r>0: # If Neuron is not in first row
            valid_connections.append((r-1,c,0)) #can go up
        if r<self.rows-1: # If Neuron is not in last row
            valid_connections.append((r+1,c,2)) #can go down 
        if c>0: # If neuron is not in first column
            valid_connections.append((r,c-1,3)) #can go left
        if c<self.cols-1: # If neuron is not in last column
            valid_connections.append((r,c+1,1)) #can go right

        return valid_connections
    
    # This method initializes the Neurons firing signals
    # Starts at the Neuron which is indicated and then proceeds based on the 
    # threshold, connection strength until the energy of signal is insufficient to trigger a fire moment
    def initialize(self, row, col, signal_strength):
        if row>0:
            row -= 1
        if col>0:
            col -= 1
        
        # Since the firing process is initialized, this has now entered the first event
        self.event_id +=1

        # A queue of Neurons to be visited
        todo_list = deque([(row,col,signal_strength)])
        while todo_list:
            r,c,s = todo_list.popleft() # Remove first in the queue
            self.current_time+=1 # Increment the current time of that Neuron by 1, since it's firing and will eventually rest
            self.energymatrix[r][c] += (self.current_time - self.last_update_map[r, c])*2 # Increase the energy of the neuron
            self.last_update_map[r, c] = self.current_time # Since the neuron has been activated once, its last_update is equal tot he current time(iteration)
            self.matrix[r][c].fired = True
            self.matrix[r][c].last_signal_id = self.event_id 

            for r_neighbor,c_neighbor,w_index in self.connections(r,c): 
                
                # Calculate the Signal Strength based on weight of connection
                s_strength = s*self.cweights[r_neighbor,c_neighbor,w_index]
                if s_strength >= self.matrix[r_neighbor][c_neighbor].threshold and self.matrix[r_neighbor][c_neighbor].last_signal_id != self.event_id:
                    todo_list.append((r_neighbor,c_neighbor,s_strength)) # Add the neuron to queue if signal can travel
                else:
                    pass
            self.energymatrix[r][c] -= 5 # Since the neuron fired it will loose 10 units of energy

    def heatmap(self):
        final_energies = self.energymatrix + (self.current_time - self.last_update_map) * 2
        plt.figure(figsize=(12, 10), dpi=200)
        sns.heatmap(final_energies,
                    cmap='rocket_r', 
                    square=True,      # Makes each neuron a perfect square
                    cbar=True,        # Shows the energy scale/legend on the side
                    xticklabels=round(self.rows/10),   # Only show a label every 10 neurons
                    yticklabels=round(self.cols/10))
        plt.show()
