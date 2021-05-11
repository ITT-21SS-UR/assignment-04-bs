# work was split equally between Erik Blank and Michael Schmidt

import os

"""
Our advanced pointing technique works through the mouse input.
The concept speeds the mouse interaction up if the mouse doesn't
touch any target. This works through switching between high and 
low CD gain. 

The filter function manipulates the X and Y coordinates of the 
mouse by reading the current mouse position and comparing it to
the coordinates of each circle center plus the diameter plus a
10px margin. If the mouse is in this space, it behaves normally, 
if the mouse is NOT in this space the movement of the mouse gets
speed up manipulating the mouse acceleration to boost the movement.
"""

"""
circleList datastructure
e.g. circleList = [{xPos: 1, yPos: 2, diameter: 10}]

mousePosition datastructure
e.g. mousePosition = {xPos: 1, yPos: 2}
"""

# TODO: 282 hard coded mouse id for acceleration needs to be removed?

class AdvancedPointing:

    def __init__(self, circleList):
        super().__init__()
        self.circleMargin = 50
        self.speedUpFactor = 1.5
        self.circleList = circleList

    # experiment needs to run the filter function in loop
    def filter(self, mousePosition):
        # check if the position is in the circle plus margin area
        inCircleArea = False
        for circle in self.circleList:
            # check if mouse is between xMinPos and xMaxPos of area
            # and between yMinPos and yMaxPos of area
            if (mousePosition["xPos"] >= (circle["xPos"] - circle["diameter"] / 2 - self.circleMargin) and
                    mousePosition["xPos"] <= (circle["xPos"] + circle["diameter"] / 2 + self.circleMargin) and
                    mousePosition["yPos"] >= (circle["yPos"] - circle["diameter"] / 2 - self.circleMargin) and
                    mousePosition["yPos"] <= (
                    circle["yPos"] + circle["diameter"] / 2 + self.circleMargin)
                ):
                inCircleArea = True
                break
            else:
                inCircleArea = False
        
        if (inCircleArea):
            # set accerlatrion to normal 0
            os.system("xinput set-prop 12 282 -1")
        else: 
            # set accerlatrion to fast 1
            os.system("xinput set-prop 12 282 0")
