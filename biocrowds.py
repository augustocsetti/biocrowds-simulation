
import sys

import pygame

from config import *
from objects.field import Field
from simulations import *
from tools.arg_parser import build_parser


class BioCrowds:
    def __init__(self, type) -> None:
        pygame.init()

        self.window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Biocrowds Simulation')
        self.window.fill(BLACK)

        self.clock = pygame.time.Clock()

        # generate markers
        self.field = Field()
        self.field.generate_markers()
        
        # initial agents AQUI
        self.agents:list = simulations[type]()

        # matrix to store the current grid of all agents
        self.current_grid = [[[] for i in range(self.field.grid_len[1])] for j in range(self.field.grid_len[0])]

    def loop(self):
        self.run = True
        while(self.run):
            self.window.fill(BLACK)

            self.event_handler()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        quit()   

    def event_handler(self):
        # Event handler
        # mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                #agents.append(Agent((mouse_pos), goal=(0, SCREENHEIGHT))) # AQUI
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:
            #         agents = agents[:-1]
        return

    def update(self):
        # cleaning grids
        for i in range(len(self.current_grid)):
            for j in range(len(self.current_grid[i])):
                self.current_grid[i][j].clear()

        # update agents grids
        for agent in self.agents:
            visible_grids = agent.sensor.check_visible_grids(self.field.grids_group)
            if visible_grids:                
                for grid in visible_grids:
                    self.current_grid[grid.position[0]][grid.position[1]].append(agent)
                #     print(grid.position, end=', ')
                # print('')

        # running grids to send only agents that are close to the markers
        for x in range(len(self.current_grid)):
            for y in range(len(self.current_grid[x])):
                if self.current_grid[x][y]:
                    self.field.set_markers_owner_by_grid(agents=self.current_grid[x][y], grid=(x, y))

        # updating agents position
        for agent in self.agents:
            agent.update(self.window)
            # check if agent hit his goal # AQUI CONTINUAR
            if not agent.on:
                self.agents.remove(agent)

    def draw(self):
        # grids
        # for grid in self.field.grids_group:
        #     grid.draw(self.window)
        # markers
        for marker in self.field.markers:
            marker.draw(self.window)
        # agents
        for agent in self.agents:
            agent.draw(self.window)

if __name__ == '__main__':

    parser = build_parser('BioCrowds Simulation. To change some simulation parameter open config.py file.')
    args = vars(parser.parse_args())

    type = args['simulation_type']

    biocrowds = BioCrowds(type)
    biocrowds.loop()
