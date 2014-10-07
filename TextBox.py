import pygame
from pygame.locals import *

pygame.font.init()

class TextBox(object):
    
    def init_props(self):
        # ------------------ Properties -----------------
        self.baseRect         = Rect((0, 0), (0, 0))
        self.width            = 0
        self.height           = 0
        self.x                = 0 
        self.y                = 0
        self.clickedX         = 0
        self.clickedY         = 0
        self.scrolling        = False
        self.backgroundColor  = (255, 255, 255)
        
        # Font and text stuff
        self.maxCharsPerLine  = 0
        self.fontWidth        = 0
        self.fontColor        = (0, 0, 0)
        self.fontSize         = 12
        self.font             = pygame.font.Font("cour.ttf", 42)
        self.text             = ""
        self.textLength       = 0
        self.lineHeight       = 0
        
        # Drawing Surfaces
        self.textSurfaces     = []
        self.answerSurfaces   = []
        self.previousSurfaces = []
        
        # Cursor 
        self.cursorPos        = 0;
        self.cursorRect       = Rect((0, 0), (0, 0))
        self.cursorColor      = (0, 0, 0)
        
        # Scroll bar
        self.scrollRectWidth  = 20
        self.scrollRect       = Rect((0, 0), (0, 0))
        self.scrollRectColor  = Rect((0, 0), (0, 0))
        self.lineYOffset      = 0
        
        self.enteredCommands  = []
        self.hasFocus         = True 
        # -----------------------------------------------

    def __init__(self, xPos, yPos, w, h, fontPath, fontSize):
        self.init_props()

        self.x               = xPos
        self.y               = yPos
        self.width           = w
        self.height          = h
        self.fontSize        = fontSize
        
        # Create the background rectangle
        self.baseRect        = Rect((self.x, self.y), (self.width, self.height))
        self.font            = pygame.font.Font(fontPath, self.fontSize)
        self.cursorRect      = Rect((0, 0), (self.font.metrics('A')[0][4], self.font.get_height()))
        self.lineHeight      = self.font.get_linesize() + 5
        self.maxCharsPerLine = self.width / self.font.metrics('A')[0][4] - 1
        self.scrollRect      = Rect((self.width - self.scrollRectWidth, 0), (self.scrollRectWidth, 40))
    
    def setFocus(value):
        self.hasFocus = value

    def draw(self, ticks):
        
        # print self.enteredCommands
        # print self.text
        
        # Draw the background
        pygame.draw.rect(pygame.display.get_surface(), self.backgroundColor, self.baseRect)
        
        if self.hasFocus:
            # Animate the cursor. Blinks every 3/4 of a second
            if ticks % 1500 < 750:
                pygame.draw.rect(pygame.display.get_surface(), self.cursorColor, self.cursorRect)
            else:
                pygame.draw.rect(pygame.display.get_surface(), self.backgroundColor, self.cursorRect)
        
        # Draw scroll rect
        if self.scrollRect.height > 0:
            pygame.draw.rect(pygame.display.get_surface(), self.scrollRectColor, self.scrollRect)

    # Called on mouse click event
    # Checks if you clicked in on the scroll rectangle
    def setClickedPos(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        
        # Check if the user is clicked on the scroll rect
        if (x >= self.scrollRect.left and x <= self.scrollRect.top + self.scrollRect.width) and (y >= self.scrollRect.top and y <= self.scrollRect.top + self.scrollRect.height):
            self.clickedX = x
            self.clickedY = y
    
    def handleScrolling(self):
        
        if pygame.mouse.get_pressed()[0]:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            
            self.scrollRect.top = y - self.scrollRect.width / 2
            
            if self.scrollRect.top + self.scrollRect.h > self.height:
                self.scrollRect.top = self.height - self.scrollRect.h
            else:
                self.scrolling = True
                self.lineYOffset = y - self.clickedY
    
    def onScrollRelease(self):
        
        self.cursorRect.y -= self.lineYOffset
        self.scrolling     = False
    
    def handleInput(self, event):
        if self.hasFocus:
            keyPressed = self.getKeyPressed(event)
            
            if keyPressed != "" and keyPressed != None and keyPressed != "back" and keyPressed != "enter" and keyPressed != "up" and keyPressed != "down":
                # Append the key pressed to the entered text
                self.text += keyPressed
                numLines = 0
                
                if len(self.text) % self.maxCharsPerLine == 0 and len(self.text) > 0:
                    
                    # Move the cursor to the next line
                    self.cursorRect.y += self.lineHeight
                    self.cursorRect.x = 0
                else:
                    # Move the cursor right by the pixel width of the last 
                    # entered character and increment cursor position
                    self.cursorRect.x += self.font.metrics(keyPressed)[0][4]
                    self.cursorPos += 1
                    
            return keyPressed
       
    def getKeyPressed(self, event):
        # print event.key
        
        # The escape key was pressed
        if event.key == 27:
        	return None

        # Enter key was pressed
        if event.key == 13 or event.key == 271:
            return "enter"

        # Delete key was pressed
        if event.key == 8:
            return "back"

        # Up arrow key pressed
        if event.key == 273:
            return "up"

        # Down arrow key pressed
        if event.key == 274:
            return "down"

        # ( pressed
        if pygame.key.get_pressed()[K_LSHIFT] and pygame.key.get_pressed()[K_9]:
            return '('

        # ) pressed
        if pygame.key.get_pressed()[K_LSHIFT] and pygame.key.get_pressed()[K_0]:
            return ')'
        if (event.key >= 97 or event.key <= 122) and not pygame.key.get_pressed()[K_LCTRL]:
            return event.unicode
        else:
            return None
