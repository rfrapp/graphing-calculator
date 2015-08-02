
from MathFunctions import *
import xml.etree.cElementTree as ET
import random

BLACK      = "#117"
LIGHTGREEN = "#00FF00"
BLUE       = "#0000FF"
DARKGREEN  = "#00AA00"
RED        = "#FF0000"

random.seed()

class CalculatorLogic(object):
    colors = [BLACK, LIGHTGREEN, BLUE, DARKGREEN, RED]

    def __init(self):
        pass

    def readTableXml(self):
      tableInfo = []

      tree = ET.parse("files/Table.xml")
      root = tree.getroot()

      tableInfo.append(root.find("start").text)
      tableInfo.append(root.find("increment").text)

      return tableInfo

    def writeGraphXml(self, equations):
      # Write an XML file with the graph equations in it
      root = ET.Element("Graphs")

      for i in equations:
        graph = ET.SubElement(root, "graph")
        graph.set("color", str(random.randrange(0, 255)) + ',' + str(random.randrange(0, 255)) + ',' + str(random.randrange(0, 175)))
        graph.text = i

      tree = ET.ElementTree(root)
      tree.write("files/graphs.xml")

    def getGraphs(self):
      graphs = []

      # read files/graphs.xml
      tree = ET.parse('files/graphs.xml')
      root = tree.getroot()

      for child in root.findall("graph"):
        graphs.append([child.text, child.get('color')])

      for i in range(len(graphs)):
        graphs[i][0] = graphs[i][0][graphs[i][0].find('=') + 1:]

      print "graphs: ", graphs

      return graphs

    def getWindow(self):
      window = []

      # read files/window.xml
      tree = ET.parse('files/window.xml')
      root = tree.getroot()

      window.append(float(root.find("xmin").text))
      window.append(float(root.find("xmax").text))
      window.append(float(root.find("ymin").text))
      window.append(float(root.find("ymax").text))
      window.append(float(root.find("xscale").text))
      window.append(float(root.find("yscale").text))

      # print "window: ", window

      return window


    def calculatePoint(self, text, x):
      text = text.replace("x", "(" + str(x) + ")")
      # print "Text:", text
      print "expression:", text
      y    = self.calculate(text)
      if not "Error" in y:
        y    = solveShuntingExpression(y)

      if not "Error" in y:
         return [x, float(y)]
      else:
        return "Error"

    def infix_to_rp(self, text):
        try:
            expression = shuntingYard(text)

            if "Error" in expression:
                return "Error"

            return expression

        except ValueError:
            return "Error"

    def calculate(self, text):
        # print "text:", text

        try:
            expression = shuntingYard(text)
            # print "expression:", expression
            solution = solveShuntingExpression(expression)

            if solution[len(solution) - 2:len(str(solution))] == ".0":
                solution = solution[:-2]
        except ValueError:
            solution = "Error"

        return solution
