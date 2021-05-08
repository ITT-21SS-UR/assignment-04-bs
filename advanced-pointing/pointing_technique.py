# work was split equally between Erik Blank and Michael Schmidt

"""
Our advanced pointing technique works through the mouse input.
The concept speeds the mouse interaction up if the mouse doesn't
touch any target. This works through switching between high and 
low CD gain. 

The filter function manipulates the X and Y coordinates of the 
mouse by reading the current mouse position and comparing it to
the coordinates of each circle center plus the diameter plus a
20px margin. If the mouse is in this space, it behaves normally, 
if the mouse is NOT in this space the movement of the mouse gets
speed up by reading the mouse input and translating it with a 
factor for the X and Y values to boost the movement.
"""


# pseude
allCircles = [{xPos, yPos, width, height
               }]


class AdvancedPointing:

    def __init__(self):
        super().__init__()

    def filter(self, targetPosition, mousePosition):
        print(targetPosition)
        print(mousePosition)
