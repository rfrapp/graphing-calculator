import pygame
from pygame.locals import *
import TextBox, CalculatorLogic

class Table(TextBox):
    graphs = []
    points = []
    
    # -------------------- Table Info ---------------------
    tblStart = 0
    tblIncrement = 1
    # -------------------- / Table Info -------------------

    maxLines = 0
    logic = CalculatorLogic.CalculatorLogic()


    def __init__(self):
        getTableInfo() 

    def getTableInfo(self):
        tblInfo = logic.getTableInfo()
        self.tblStart = float(tblInfo[0])
        self.tblIncrement = float(tblInfo[1])

    def initialCalculation(self):
        for i in range(tblStart, )

