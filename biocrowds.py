
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
        print('Generating markers...')
        self.field.generate_markers()
        
        # initial agents AQUI
        print('Generating agents...')
        self.agents:list = simulations[type]()

        # matrix to store the current grid of all agents
        self.current_grid = [[[] for i in range(self.field.grid_len[1])] for j in range(self.field.grid_len[0])]

        # draw control
        self.draw_sensor = False
        self.draw_grid = False
        self.draw_mark = False

        print('All done!')

    def loop(self):
        self.start = False
        self.run = True
        while(self.run):
            self.window.fill(BLACK)

            self.event_handler()
            if self.start:
                self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        quit()   

    def event_handler(self):
        # Event handler
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.agents.append(Agent((mouse_pos), goal=(random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT)))) # AQUI
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start = not self.start
                if event.key == pygame.K_g:
                    self.draw_grid = not self.draw_grid
                if event.key == pygame.K_m:
                    self.draw_mark = not self.draw_mark                   
                if event.key == pygame.K_r:
                    self.agents.pop()                    
                if event.key == pygame.K_s:
                    self.draw_sensor = not self.draw_sensor                  
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

        # running grids to send only agents that are close to the markers
        for x in range(len(self.current_grid)):
            for y in range(len(self.current_grid[x])):
                if self.current_grid[x][y]:
                    self.field.set_markers_owner_by_grid(agents=self.current_grid[x][y], grid=(x, y))
                else:
                    for marker in self.field.grids_markers[x][y]:
                        marker.set_color(marker.color_base)

        # updating agents position
        for agent in self.agents:
            agent.update(self.window)
            # check if agent hit his goal # AQUI CONTINUAR
            if not agent.on:
                self.agents.remove(agent)

    def draw(self):
        # elements of field
        self.field.draw(self.window, self.draw_grid, self.draw_mark)
        # agents
        for agent in self.agents:
            agent.draw(self.window, self.draw_sensor)

    def print_instructions(self):
        print('\n- Instructions:')
        print('\tSPACE BAR    Start/Stop simulation.')
        print('\tON CLICK     Add a agent at mouse position with a random goal.')
        print('\tG            Turn on/off grids draw.')
        print('\tM            Turn on/off markers draw.')
        print('\tR            Delete last agent created.')
        print('\tS            Turn on/off sensor draw.')
        
        print('\nYou also can change all parameters playing with config.py file and, on simulation.py file by changing the parameters from simulations functions')

if __name__ == '__main__':

    print('# BioCrowds Simulation')

    parser = build_parser('BioCrowds Simulation. To change some simulation parameter open config.py file.')
    args = vars(parser.parse_args())

    type = args['simulation_type']

    biocrowds = BioCrowds(type)
    biocrowds.print_instructions()
    biocrowds.loop()
