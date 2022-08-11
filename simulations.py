import random

from numpy import array

from objects.agent import Agent
from config import *


def simulation_0(quantity=N_AGENTS):
    agents = []
    for i in range(quantity):
        agents.append(Agent(position=(SCREENWIDTH-50, 50), goal=(0, SCREENHEIGHT)))
    return agents

def simulation_1(goals=None, positions=None, quantities=N_AGENTS):
    # if not goal:
    #     goal = 1
    # AQUI CONTINUAR
    agents = []

    # team 1
    for _ in range(quantities):
        agents.append(Agent(position=(SCREENWIDTH - GRID/2, GRID/2), goal=(0, SCREENHEIGHT), color=BLUE))
    # team 2
    for _ in range(quantities):
        agents.append(Agent(position=(GRID/2, GRID/2), goal=(SCREENWIDTH, SCREENHEIGHT), color=RED))

    return agents

def simulation_2(quantities=N_AGENTS, lines=LINES):
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

simulations = {
    '0': simulation_0,
    '1': simulation_1,
    '2': simulation_2,
}
