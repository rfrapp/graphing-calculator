import pygame, sys, Calculator, GraphList, Graph
from pygame.locals import *


class CalculatorProgram():
    
    # ------------------ Properties -----------------
    # Screen attributes
    screenWidth    = 640
    screenHeight   = 480

    # Create the screen
    screen         = pygame.display.set_mode((screenWidth, screenHeight))
    
    # Constants for the font
    fontPath       = "cour.ttf"
    fontSize       = 42
    
    # Objects for the calculator menus
    calc           = Calculator.Calculator(0, 0, screenWidth, screenHeight, fontPath, fontSize)
    graphList      = GraphList.GraphList(0, 0, screenWidth, screenHeight, fontPath, fontSize)
    graph          = Graph.Graph(0, 0, screenWidth, screenHeight, fontPath, fontSize)

    # Booleans for different menus
    mainMenu       = True
    showGraph      = False
    graphLinesMenu = False
    # -----------------------------------------------

    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()

    def execute(self):
        # The game loop
        while True:
            for event in pygame.event.get():
                self.handleInput(event)
                
                if self.mainMenu:
                    if event.type == KEYDOWN:
                        self.calc.handleInput(event)
                    
                    if event.type == MOUSEBUTTONDOWN:
                        self.calc.setClickedPos()
                    
                    if event.type == MOUSEMOTION:
                        self.calc.handleScrolling()
                    
                    if event.type == MOUSEBUTTONUP:
                        self.calc.onScrollRelease()
                
                elif self.showGraph:
                    if event.type == MOUSEMOTION:
                        self.graph.handleMouseMotion()
                    if event.type == KEYDOWN:
                        self.graph.handleInput(event)
                    if event.type == MOUSEBUTTONDOWN:
                        self.graph.handleMouseClick(event)

                elif self.graphLinesMenu:
                    if event.type == KEYDOWN:
                        self.graphList.handleInput(event)
                    
                    if event.type == MOUSEBUTTONDOWN:
                        self.graphList.setClickedPos()
                    
                    if event.type == MOUSEMOTION:
                        self.graphList.handleScrolling()
                    
                    if event.type == MOUSEBUTTONUP:
                        self.graphList.onScrollRelease()
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Clear the screen
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((0, 0), (self.screenWidth, self.screenHeight)))

            # Draw the calculator UI to the screen
            if self.mainMenu:
                self.calc.draw(pygame.time.get_ticks())
            elif self.graphLinesMenu:
                self.graphList.draw(pygame.time.get_ticks())
            elif self.showGraph:
                self.graph.draw()
            
            pygame.display.update()

        pygame.font.quit()

    def handleInput(self, event):
        self.getKeySequence()
        
    def getKeySequence(self):
        
        # Go to graph if Ctrl+g is pressed
        if pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_g]:
            if self.graphLinesMenu == True:
                self.graphList.onExit()
                self.graph.calculateGraphs()
            
            self.mainMenu                   = False 
            self.showGraph                  = True 
            self.graphLinesMenu             = False 
            
        # Go to graph lines menu if Ctrl+y is pressed
        elif pygame.key.get_pressed()[K_LCTRL] and pygame.key.get_pressed()[K_y]:
            self.mainMenu                   = False
            self.graphLinesMenu             = True
            self.showGraph                  = False
            
        # Go back to the main menu if escape key is pressed
        elif pygame.key.get_pressed()[K_ESCAPE]:
            
            if self.graphLinesMenu == True:
                self.graphList.onExit()
                self.graph.calculateGraphs()
            
            self.mainMenu = True 
            self.graphLinesMenu = False 
            self.showGraph = False

