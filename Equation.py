
import CalculatorLogic
from CalculatorLogic import *

class Equation(object):

    def __init__(self, text, color):
        self.color       = color

        # contains a list of lists with each list
        # holding lists of x,y positions computed by substituting
        # values in the graph menu's window into the equation
        # and evaluating
        #
        # example:
        # lines    = [
        #               [[1,-1], [0,0], [1,1]] # line 1
        #               [[2,2], [3,3], [4,4]]  # line 2
        #            ]
        self.lines       = []

        # contains a list of lists with each list
        # holding lists of x,y positions converted to pixels
        self.pixel_lines = []

        # the string containing the equation text
        # ex. "x^2"
        self.value       = text

        # object to perform the calculator's logic
        self.logic       = CalculatorLogic()

    def points_to_pixels(self, w, h, window):

        # Calculate the margin for each line of the grid along x axis
        dx = w / (window[1] - window[0])

        # Calcualte the margin for each line of the grid along y axis
        dy = h / (window[3] - window[2])

        for line in self.lines:
            pixel_line = []

            for point in line:
                p = [point[0], point[1]]
                p[0] = float(point[0])
                p[1] = float(point[1])
                p[0] = w / 2 + dx * p[0]
                p[1] = h / 2 - dy * p[1]

                pixel_line.append(p)

            self.pixel_lines.append(pixel_line)

    def color_tuple(self):
        rgba = self.color.split(",")

        if len(rgba) not in (3, 4):
            return (0, 0, 0)
        return tuple(map(int, rgba))


    def calculate(self, x):
        result = self.logic.calculatePoint(self.value, x)[1]

        try:
            if "Error" in str(result):
                return "Error"
            else:
                return result
        except:
            return "Error"

    def calculate_points(self, xmin, xmax, inc = 0.5):
        line = []
        i = xmin

        while i <= xmax:
            print self.value, i
            point = self.logic.calculatePoint(self.value, i)

            if "Error" in point:
                point = self.logic.calculatePoint(self.value, i - inc / 5)
                line.append(point)

                self.lines.append(line)
                line = []

                point = self.logic.calculatePoint(self.value, i + inc / 5)
                line.append(point)

            else:
                line.append(point)

            if i + inc > xmax:
                self.lines.append(line)

            i += inc
