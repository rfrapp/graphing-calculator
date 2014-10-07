import pygame
from pygame.locals import *
from TextBox import *
from CalculatorLogic import *

class GraphList(TextBox):
    
    def __str__(self):
        return "GraphList"
    
    def __init__(self, xPos, yPos, w, h, fontPath, fontSize):
        # ------------------ Properties -----------------
        self.graphs = []
        self.logic  = CalculatorLogic()
        # -----------------------------------------------

        super(GraphList, self).__init__(xPos, yPos, w, h, fontPath, fontSize)
        self.enteredCommands = []
        
        self.graphs          = self.logic.getGraphs()
        count = 1

        for graph in self.graphs:
        	self.enteredCommands.append("Y" + str(count) + "=" + graph[0])
        	count += 1

        self.text = "Y" + str(len(self.graphs) + 1) + "="
        self.cursorRect.x = self.font.metrics("Y")[0][4] * len(self.text)
        self.cursorRect.y = self.lineHeight * (len(self.enteredCommands))

    def getTextHeight(self):
        numLines = 0
        
        # Get the number of lines for previously entered commands and answers
        for i in self.enteredCommands:
            for j in range(len(i)):
                if j % self.maxCharsPerLine == 0:
                    numLines += 1
        
        # Get the number of lines needed
        for i in range(len(self.text)):
            if i % self.maxCharsPerLine == 0:
                numLines += 1
        
        # Count the line that is about to be entered
        numLines += 2
        
        # Get extra height of surfaces
        return numLines * self.font.get_height() + numLines - 1 * self.lineHeight

    def draw(self, ticks):
    	super(GraphList, self).draw(ticks)

    	self.drawText(True)
        
        totalHeight = self.getTextHeight()
        extraHeight = totalHeight - self.height
        
        if extraHeight > 0:
            self.scrollRect.height = self.height - extraHeight
        else:
            self.scrollRect.height = 0

    def onExit(self):
        # if an equation was entered but the user didn't 
        # click 'enter' afterwards
        if self.text != "" and self.text.find('=') != len(self.text) - 1:
            # save the equation to the entered commands
            self.enteredCommands.append(self.text)

            # start a new command
            self.text = "Y" + str(len(self.enteredCommands) + 1) + "="
            
            # set the cursor position to the new command
            self.cursorRect.x = self.font.metrics("Y")[0][4] * len(self.text)
            self.cursorRect.y = self.lineHeight * (len(self.enteredCommands))

        # write the equations to an XML file
        self.logic.writeGraphXml(self.enteredCommands)

    def drawText(self, useOffset = False):
        # print "Drawing with", self
        
        # Get the number of commands entered previously
        startY                = 0
        self.textSurfaces     = []
        self.previousSurfaces = []
        numLines              = 0
        count                 = 0
        
        # Get surfaces for the previously entered commands
        for i in self.enteredCommands:
            
            if i != "":
                pNumLines = 0
                self.previousSurfaces.insert(count, [])
                
                # Get the number of lines for each previously entered command
                for j in range(len(i)):
                    if j % self.maxCharsPerLine == 0:
                        pNumLines += 1
                        
                # Insert surfaces to prevous surface list
                for j in range(pNumLines):
                    self.previousSurfaces[count].insert(j, self.font.render(i[j * self.maxCharsPerLine: (j + 1) * self.maxCharsPerLine], True, self.fontColor))
                
                count += 1
                
        # Draw the previously entered commands
        for i in range(len(self.previousSurfaces)):
            for j in self.previousSurfaces[i]:
                pygame.display.get_surface().blit(j, (0, startY - self.lineYOffset))
                startY += self.lineHeight
        
        # Get the number of lines of entered text
        for i in range(len(self.text)):
            if i % self.maxCharsPerLine == 0:
                numLines += 1
                            
        # Create the text surfaces
        for i in range(numLines):
            self.textSurfaces.insert(i, self.font.render(self.text[i * self.maxCharsPerLine: (i + 1) * self.maxCharsPerLine], True, self.fontColor))
        
        if useOffset:
            # Draw the surfaces
            for i in self.textSurfaces:
                pygame.display.get_surface().blit(i, (0, startY - self.lineYOffset))
                startY += self.lineHeight
        else:
            # Draw the surfaces
            for i in self.textSurfaces:
                pygame.display.get_surface().blit(i, (0, startY))
                startY += self.lineHeight
     

    def handleInput(self, event):
        keyPressed = super(GraphList, self).handleInput(event)

        if keyPressed == '=':
            # prevent input of = sign
            self.text = self.text[:-1]
            self.cursorRect.left -= self.font.metrics("A")[0][4]

        if keyPressed == "enter":
            # add the command to the entered commands list
            # and the graphs list
            self.enteredCommands.append(self.text)
            self.graphs.append(self.text)
            
            # start a new Y=
            self.text          = "Y" + str(len(self.graphs) + 1) + "="
            self.cursorRect.y += self.lineHeight
            self.cursorRect.x  = self.font.metrics("Y")[0][4] * (2 + len(str(len(self.graphs))))

        # user pressed the delete key
        elif keyPressed == "back":
            
            if len(self.text) >= 1:
                # Get the width of the last character for moving the cursor
                widthToMoveBack = self.font.metrics(self.text[len(self.text) - 1])[0][4]
            
            # Remove the last character of the string
            # Subtract 1 from the cursor position
            
            if len(self.text) >= 1:

                # if the last character in the text being entered
                # is not an '=', then remove the last character
                # of the text and subtract 1 from the cursor
                # position
                if self.text[-1] != '=':
                    self.text = self.text[:-1]
                    self.cursorPos -= 1
                else:
                    # If the user is not editing Y1
                    if len(self.enteredCommands) != 0 and len(self.graphs) != 0:
                        
                        # Set the entered text = to the text from the previous
                        # Y= line, remove that line from the entered commands
                        # and adjust the cursor x and y
                        self.text = self.enteredCommands[len(self.enteredCommands) - 1]
                        self.enteredCommands = self.enteredCommands[:-1]
                        self.graphs = self.graphs[:-1]
                        self.cursorRect.y -= self.lineHeight
                        self.cursorRect.x = (len(self.text) % self.maxCharsPerLine + 1) * self.font.metrics('A')[0][4]
                    else:
                        # the user is editing the line "Y1=", prevent
                        # the cursor from moving backwards
                        widthToMoveBack = 0

            # if the user deleted the last character in a line
            if (len(self.text) + 1) % self.maxCharsPerLine == 0:
                if self.cursorRect.y != 0:
                    self.cursorRect.y -= self.lineHeight
                    self.cursorRect.x = self.maxCharsPerLine * self.font.metrics('A')[0][4]
            
            if len(self.text) >= 1:
                # Move the cursor left the width of the deleted character
                self.cursorRect.x -= widthToMoveBack
            else:
                self.cursorRect.x = 0
