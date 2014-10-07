import pygame, Equation
from Equation import *
from TextBox import *
from pygame.locals import *
import xml.etree.ElementTree as ET
from math import *
from CalculatorLogic import *
import random

class Graph(TextBox):

    def init_properties(self):

        # List 
        # <structure>
        # [0] = xmin   (float)
        # [1] = xmax   (float)
        # [2] = ymin   (float)
        # [3] = ymax   (float)
        # [4] = xscale (float)
        # [5] = yscale (float)
        # </structure>
        self.window      = []
        self.equations   = []
        self.logic       = CalculatorLogic()
        self.printCount  = 0

        # Surfaces for trace display
        self.xSurface    = None 
        self.ySurface    = None 

        # String values to put into trace surfaces
        self.xTrace      = ""
        self.yTrace      = ""

        self.trace_mode      = False
        self.trace_inc       = 0.1
        self.trace_select    = False
        self.trace_x         = 0
        self.trace_position  = []
        self.trace_reticle   = None 
        self.trace_index     = -1
        self.message_surface = None 
        self.message         = ""
        self.color_rects     = []

    def __init__(self, xPos, yPos, w, h, fontPath, fontSize):
        self.init_properties()

        super(Graph, self).__init__(xPos, yPos, w, h, fontPath, fontSize)

        self.window = self.logic.getWindow()
        self.trace_x = self.window[0]
        self.calculateGraphs()
        self.xSurface = self.font.render(self.xTrace, True, self.fontColor)
        self.ySurface = self.font.render(self.yTrace, True, self.fontColor)

    def calculateGraphs(self):
        self.equations = []

        for eq in self.logic.getGraphs():
            equation = Equation(eq[0], eq[1])
            self.equations.append(equation)
        
        for i in range(len(self.equations)):
            self.equations[i].calculate_points(self.window[0], self.window[1], 0.5)

        self.pointsToPixels()

    def draw(self):
        self.drawGrid()
        self.drawLines()

        if self.trace_mode:
            # draw color select menu
            if self.trace_select:
                colorbox_height = 40
                bg_rect = Rect(10, 10, 40, colorbox_height * (len(self.equations)))
                outline_rect = Rect(bg_rect.left - 2, bg_rect.top - 2,
                                    bg_rect.width + 4, bg_rect.height + 4)

                # draw outline rectangle
                pygame.draw.rect(pygame.display.get_surface(), 0x000000, outline_rect)

                # draw background rectangle
                pygame.draw.rect(pygame.display.get_surface(), 0xFFFFFF, bg_rect)

                # draw the color squares
                for i in range(len(self.equations)):
                    pygame.draw.rect(pygame.display.get_surface(), self.equations[i].color_tuple(), self.color_rects[i])

                # draw message
                pygame.display.get_surface().blit(self.message_surface, (self.width - self.message_surface.get_width() - 10, 10))

            else:
                colorbox_height = 40
                bg_rect = Rect(10, 10, 40, colorbox_height)
                outline_rect = Rect(bg_rect.left - 2, bg_rect.top - 2,
                                    bg_rect.width + 4, bg_rect.height + 4)
                color_rect = Rect(bg_rect.left + 2, bg_rect.top + 2, 
                                  bg_rect.width - 4, bg_rect.height - 4)

                # draw outline rectangle
                pygame.draw.rect(pygame.display.get_surface(), 0x000000, outline_rect)

                # draw background rectangle
                pygame.draw.rect(pygame.display.get_surface(), 0xFFFFFF, bg_rect)

                pygame.draw.rect(pygame.display.get_surface(), self.equations[self.trace_index].color_tuple(), color_rect)

                # draw trace reticle 
                pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (int(self.trace_position[0]), int(self.trace_position[1]))    , 4)


            # Draw trace surfaces
            pygame.display.get_surface().blit(self.xSurface, (10, pygame.display.get_surface().get_height() - 52))
            pygame.display.get_surface().blit(self.ySurface, (pygame.display.get_surface().get_width() / 2 + 42, pygame.display.get_surface().get_height() - 52))


    def drawLines(self):
        count = 0

        for equation in self.equations:
            for line in equation.pixel_lines:
                pygame.draw.lines(pygame.display.get_surface(), equation.color_tuple(), False, line, 2)
                count += 1

    def pointsToPixels(self):        
        for i in range(len(self.equations)):
            self.equations[i].points_to_pixels(self.width, self.height, self.window)

    def handleMouseClick(self, event):
        if self.trace_select:
            # get the mouse position
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]

            graph_clicked = False 

            # check for collision between mouse and
            # one of the color rectangles
            for i in range(len(self.color_rects)):
                if self.color_rects[i].collidepoint(x, y):
                    self.trace_select = False
                    self.trace_mode   = True 
                    graph_clicked = True
                    self.trace_index = i  
                    print "clicked graph"
                    break 

            # if a color rectangle was clicked
            if graph_clicked:
                # get the first point of the first line of the selected
                # equation
                self.change_trace_point()

    def point_to_pixel(self, x, y):
        # Calculate the margin for each line of the grid along x axis
        dx = self.width / (self.window[1] - self.window[0])

        # Calcualte the margin for each line of the grid along y axis
        dy = self.height / (self.window[3] - self.window[2])

        x = float(x)
        y = float(y)
        x = self.width / 2 + dx * x
        y = self.height / 2 - dy * y

        return [x, y]

    def change_trace_point(self, x_shift = 0):
        self.trace_x += x_shift 
        trace_y   = self.equations[self.trace_index].calculate(self.trace_x)

        self.xTrace  = "X=" + str(round(self.trace_x, 4))
        self.yTrace  = "Y=" + str(round(float(trace_y), 4))

        self.xSurface = self.font.render(self.xTrace, True, self.fontColor)
        self.ySurface = self.font.render(self.yTrace, True, self.fontColor)

        self.trace_position = self.point_to_pixel(self.trace_x, trace_y)

    def handleInput(self, event):
        if event.key == K_LEFT:
            # if a graph has been selected
            if self.trace_mode and not self.trace_select:
                if self.trace_x - self.trace_inc >= self.window[0]:
                    self.change_trace_point(-self.trace_inc)

        elif event.key == K_RIGHT:
            # if a graph has been selected
            if self.trace_mode and not self.trace_select:
                if self.trace_x + self.trace_inc <= self.window[1]:
                    self.change_trace_point(self.trace_inc)

        elif event.key == K_UP:
            # if a graph has been selected
            if self.trace_mode and not self.trace_select:
                if self.trace_index - 1 >= 0:
                    self.trace_index -= 1 
                    self.change_trace_point()               

        elif event.key == K_DOWN:
            # if a graph has been selected
            if self.trace_mode and not self.trace_select:
                if self.trace_index + 1 < len(self.equations):
                    self.trace_index += 1

                    self.change_trace_point()

        elif event.key == K_t:

            if not self.trace_mode:
                # enter trace mode
                self.trace_mode = True 
                self.trace_select = True 

                # create the color rects
                self.color_rects = []

                startX = 12
                startY = 12

                colorbox_height = 40
                bg_rect = Rect(10, 10, 40, colorbox_height * (len(self.equations)))
                outline_rect = Rect(bg_rect.left - 2, bg_rect.top - 2,
                                    bg_rect.width + 4, bg_rect.height + 4)

                for i in range(len(self.equations)):
                    color_rect = Rect(startX, startY, bg_rect.width - 4, colorbox_height - 4)
                    startY += colorbox_height
                    self.color_rects.append(color_rect)

                self.message = "Select a graph..."
                self.message_surface = self.font.render(self.message, True, self.fontColor)

            else:
                self.trace_mode = False
                self.trace_select = False
                self.trace_index = -1
                self.xTrace = ""
                self.yTrace = ""
                self.xSurface = self.font.render(self.xTrace, True, self.fontColor)
                self.ySurface = self.font.render(self.yTrace, True, self.fontColor)


    def handleMouseMotion(self):
        pass 
        # width = pygame.display.get_surface().get_width()
        # height = pygame.display.get_surface().get_height()

        # # Calculate the margin for each line of the grid along x axis
        # dx = width / (self.window[1] - self.window[0])

        # # Calcualte the margin for each line of the grid along y axis
        # dy = height / (self.window[3] - self.window[2])

        # # Tuple with (x, y) of mouse 
        # mousePos = pygame.mouse.get_pos()

        # if pygame.display.get_surface().get_at((mousePos[0], mousePos[1])) == (1, 1, 1):
        #     self.xTrace = "X=" + str(round(mousePos[0] / dx - (width / 2) / dx, 2))
        #     self.yTrace = "Y=" + str(round((mousePos[1] / dy - (height / 2) / dy) * -1, 2))
        # else:
        #     self.xTrace = ""
        #     self.yTrace = ""

        # self.xSurface = self.font.render(self.xTrace, True, self.fontColor)
        # self.ySurface = self.font.render(self.yTrace, True, self.fontColor)

    def drawGrid(self):

        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()

        # Calculate the margin for each line of the grid along x axis
        dx = width / (self.window[1] - self.window[0])

        # Calcualte the margin for each line of the grid along y axis
        dy = height / (self.window[3] - self.window[2])

        # Draw center lines for grid
        pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (0, height / 2), (width - 1, height / 2))
        pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (width / 2, 0), (width / 2, height))

        count = dx

        # Draw x markers
        while count <= width:
            pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (count, height / 2 - 10), (count, height / 2 + 10))
            count += dx

        count = dy 

        # Draw y markers 
        while count <= height:
            pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (width / 2 - 10, count), (width / 2 + 10, count))
            count += dy 
