import pygame, sys
from CalculatorLogic import *
from pygame.locals import *
from TextBox import *

pygame.font.init()

class Calculator(TextBox):
	
    # ------------------ Properties -----------------
    logic                = CalculatorLogic()
    answers              = []
    previousCommandIndex = 0
    # -----------------------------------------------


    def __str__(self):
        return "Calculator"
    
    def __init__(self, xPos, yPos, w, h, fontPath, fontSize):
        super(Calculator, self).__init__(xPos, yPos, w, h, fontPath, fontSize)
        self.enteredCommands.append("")
      
    def draw(self, ticks):
    	super(Calculator, self).draw(ticks)

    	self.drawText(True)
        
        totalHeight = self.getTextHeight()
        extraHeight = totalHeight - self.height
        
        if extraHeight > 0:
            self.scrollRect.height = self.height - extraHeight
        else:
            self.scrollRect.height = 0

    def drawText(self, useOffset = False):
        # print "Drawing with", self
        
        # Get the number of commands entered previously
        startY = 0
        self.textSurfaces = []
        self.previousSurfaces = []
        self.answerSurfaces = []
        numLines = 0
        count = 0
        
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
        
        # Get surfaces for the answers
        for i in range(len(self.answers)):
            self.answerSurfaces.insert(i, self.font.render(self.answers[i], True, self.fontColor))
                    
        # Draw the previously entered commands
        for i in range(len(self.previousSurfaces)):
            # print "len i =", len(i)
            for j in self.previousSurfaces[i]:
                pygame.display.get_surface().blit(j, (0, startY - self.lineYOffset))
                startY += self.lineHeight
            
            if len(self.answerSurfaces) == len(self.previousSurfaces):
                pygame.display.get_surface().blit(self.answerSurfaces[i], (self.width - (self.font.metrics("A")[0][4] * len(self.answers[i])) - self.scrollRect.width, startY - self.lineYOffset))
                startY += self.lineHeight
        
        # Get the number of lines of entered text
        for i in range(len(self.text)):
            if i % self.maxCharsPerLine == 0:
                numLines += 1
                            
        # Create the surfaces
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
     
        
    def getTextHeight(self):
        numLines = 0
        
        # Get the number of lines for previously entered commands and answers
        for i in self.enteredCommands:
            for j in range(len(i)):
                if j % self.maxCharsPerLine == 0:
                    numLines += 1
            
            # Add 1 to num lines to compensate for the command's answer line
            numLines += 1
        
        # Get the number of lines needed
        for i in range(len(self.text)):
            if i % self.maxCharsPerLine == 0:
                numLines += 1
        
        # Count the line that is about to be entered
        numLines += 2
        
        # Get extra height of surfaces
        return numLines * self.font.get_height() + numLines - 1 * self.lineHeight

        
    def handleInput(self, event):
        
        keyPressed = super(Calculator, self).handleInput(event)
        
        if keyPressed == "up":
            if self.previousCommandIndex + 1 < len(self.enteredCommands):
                # Move up in the list of previously entered commands
                self.previousCommandIndex += 1
                
                # Move the cursor
                self.cursorRect.x = self.font.metrics("A")[0][4] * len(self.enteredCommands[self.previousCommandIndex]) 
                
                # Change text to that command
                self.text = self.enteredCommands[self.previousCommandIndex]
            pass
        
        elif keyPressed == "down":
            if self.previousCommandIndex >= 1:
                # Move down in the list of previously entered commands
                self.previousCommandIndex -= 1
            
                # Move the cursor
                self.cursorRect.x = self.font.metrics("A")[0][4] * len(self.enteredCommands[self.previousCommandIndex]) 
            
                # Change text to that command
                self.text = self.enteredCommands[self.previousCommandIndex]
            pass
        
        elif keyPressed == "enter":
            if self.text != "":
                if "clear" in self.text:
                    # Clear the entered commands
                    self.enteredCommands = []
                    self.cursorRect.top = 0
                elif "exit" in self.text:
                    # Close the program
                    pygame.quit()
                    sys.exit()
                else:
                    # Evaluate the expression in text
                    a = self.logic.calculate(self.text)
                    
                    # Move the cursor down two lines
                    self.cursorRect.y += (2 * self.lineHeight)
                    
                    # Add the text to the entered commands list
                    self.enteredCommands.append(self.text)
                    
                    # Add the answer to the answer's list
                    self.answers.append(str(a))
                
                # Reset Text
                self.text = ""
                
                # Move the cursor back to the top left
                self.cursorRect.x = 0

        elif keyPressed == "back":
            
            if len(self.text) >= 1:
                # Get the width of the last character for moving the cursor
                widthToMoveBack = self.font.metrics(self.text[len(self.text) - 1])[0][4]
            
            # Remove the last character of the string
            # Subtract 1 from the cursor position
            
            if len(self.text) >= 1:
                self.text = self.text[:-1]
                self.cursorPos -= 1
            
            if (len(self.text) + 1) % self.maxCharsPerLine == 0:
                if self.cursorRect.y != 0:
                    self.cursorRect.y -= self.lineHeight
                    self.cursorRect.x = self.maxCharsPerLine * self.font.metrics('A')[0][4]
            
            if len(self.text) >= 1:
                # Move the cursor left the width of the deleted character
                self.cursorRect.x -= widthToMoveBack
            else:
                self.cursorRect.x = 0
