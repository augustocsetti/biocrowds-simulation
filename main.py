import random
import sys

import pygame
from numpy import array

from agent import Agent
from config import *
from marker import Field


def draw_grids(window):
    for x in range(0, SCREENWIDTH, GRID):
        pygame.draw.line(window, WHITE, (x, 0), (x, SCREENHEIGHT))
    for y in range(0, SCREENHEIGHT, GRID):
        pygame.draw.line(window, WHITE, (0, y), (SCREENWIDTH, y))

# simulations

def simulation_0(quantity=10):
    agents = []
    for i in range(quantity):
        agents.append(Agent(position=(SCREENWIDTH-50, 50), goal=(0, SCREENHEIGHT)))
    return agents

def simulation_1(goals=None, positions=None, quantities=10):
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

def simulation_2(quantities=10, lines=2):
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

if __name__ == '__main__':

    args = sys.argv[1:]

    pygame.init()

    window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Biocrowds Simulation")
    window.fill(BLACK)

    clock = pygame.time.Clock()

    # generate markers
    field = Field()
    field.generate_markers()
    
    # initial agents AQUI
    agents = []
    agents = simulations[args[0]]()

    # matrix to store the current grid of all agents
    current_grid = [[[] for i in range(field.grid_len[1])] for j in range(field.grid_len[0])]

    run = True
    while(run):
        window.fill(BLACK)

        # Event handler
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #agents.append(Agent((mouse_pos), goal=(0, SCREENHEIGHT))) # AQUI CONTINUAR
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    agents = agents[:-1]

        # cleaning grid
        for i in range(len(current_grid)):
            for j in range(len(current_grid[i])):
                current_grid[i][j].clear()

        # update grid
        for agent in agents:
            x, y = agent.grid
            current_grid[x][y].append(agent)

        # running grids to send only agents that are close to the markers
        for x in range(len(field.current_grid)):
            for y in range(len(field.current_grid[x])):
                if current_grid[x][y]:
                    field.set_markers_owner_by_grid(current_grid[x][y], (x, y))

        # draw markers and grid
        # for marker in field.markers:
        #     marker.draw(window)
        # draw_grids(window)

        for agent in agents:
            agent.update(window)

            # check if agent hit his goal AQUI CONTINUAR
            if agent.on:
                agent.draw(window)
            else:
                agents.remove(agent)
                
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()                       
