#!/usr/bin/python3
# file was written by Michael Schmidt

import os

"""
Our advanced pointing technique works through the mouse input.
The concept slows the mouse down if the mouse is in an area near a circle.
This works through switching between high and low CD gain.

The filter function manipulates the acceleration of the
mouse by reading the current mouse position and comparing it to
the coordinates of each circle center plus the diameter plus a
margin. If the mouse is in this space, it gets slowed down,
if the mouse is NOT in this space the movement of the mouse
behaves normally.
"""

"""
circleList datastructure
e.g. circleList = [{xPos: 1, yPos: 2, diameter: 10}]

mousePosition datastructure
e.g. mousePosition = {xPos: 1, yPos: 2}
"""


class AdvancedPointing:

    def __init__(self, circleList, accelId):
        super().__init__()
        self.circleMargin = 50
        self.speedUpFactor = 1.5
        self.circleList = circleList
        self.accelId = accelId

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
                    circle["yPos"] + circle["diameter"] / 2 + self.circleMargin)):
                inCircleArea = True
                break
            else:
                inCircleArea = False

        if (inCircleArea):
            # set acceleration to slow down -1
            os.system("xinput set-prop 12 " + self.accelId + " -1")
        else:
            # set acceleration to normal 0
            os.system("xinput set-prop 12 " + self.accelId + " 0")
