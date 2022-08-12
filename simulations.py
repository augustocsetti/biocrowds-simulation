import math

import random

from numpy import array

from config import *
from objects.agent import Agent


def simulation_0(num_agents=N_AGENTS):
    '''
    One group going to its goal
    '''
    agents = []
    for _ in range(num_agents):
        agents.append(Agent(position=(SCREENWIDTH-50, 50), goal=(0, SCREENHEIGHT)))
    return agents

def simulation_1(goals=None, positions=None, quantities=N_AGENTS): # AQUI CONTINUAR
    '''
    Crossing two groups in 'X' formation
    '''
    agents = []

    # team 1
    for _ in range(quantities):
        agents.append(Agent(position=(SCREENWIDTH - GRID/2, GRID/2), goal=(0, SCREENHEIGHT), color=BLUE))
    # team 2
    for _ in range(quantities):
        agents.append(Agent(position=(GRID/2, GRID/2), goal=(SCREENWIDTH, SCREENHEIGHT), color=RED))

    return agents

def simulation_2(quantities=N_AGENTS, lines=LINES):
    '''
    Crossing two groups created each side at the screen
    '''
    agents = []
    for line in range (0, lines):
        for _ in range(quantities):
            pos = array((+line*GRID, random.randint(0, SCREENHEIGHT-1)))
            goal = pos + (SCREENWIDTH, pos[1])
            agents.append(Agent(pos, goal, GREEN))
    for line in range (0, lines):
        for _ in range(quantities):
            pos = array((SCREENWIDTH-line*GRID - 1, random.randint(0, SCREENHEIGHT-1)))
            goal = pos + (-pos[0], 0)
            agents.append(Agent(pos, goal, PURPLE))
    return agents

def simulation_3(num_agents=N_AGENTS, radius=SCREENHEIGHT/2, lines=LINES, color=None):
    '''
    A circle group going to the oposite position
    '''
    agents = []
    center = array((SCREENWIDTH/2, SCREENHEIGHT/2))
    step = 360//num_agents
    for angle in range(0, 360, step):
        for line in range(0, lines):
            x = math.cos(math.radians(angle))*(radius-VISION*2*line)
            y = math.sin(math.radians(angle))*(radius-VISION*2*line)
            pos = center + array((x, y))
            goal = center - array((x, y))
            agents.append(Agent(pos, goal, color))  
    return agents

simulations = {
    '0': simulation_0,
    '1': simulation_1,
    '2': simulation_2,
    '3': simulation_3,
}
