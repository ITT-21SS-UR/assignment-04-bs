#!/usr/bin/python3

""" Copyright 2014-2018 Raphael Wimmer <raphael.wimmer@ur.de> 
License: CC-0 (essentially: do what you want with it, no attribution required)
"""

import sys
import random
import math
import itertools
from PyQt5 import QtGui, QtWidgets, QtCore
import pandas as pd
from pointing_technique import AdvancedPointing

""" setup file looks like this:
USER: 1
WIDTHS: 35, 60, 100, 170
ADVANCED_POINTING: 1 ### 0 off, 1 on
"""

FIELDS = ["timestamp", "id", "advanced_pointing", "trial", "distance", "target_size",
          "time_in_ms", "click_offset_x", "click_offset_y"]


class FittsLawModel(object):

    def __init__(self, user_id, sizes, advanced_pointing):
        print(advanced_pointing)
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.advanced_pointing = advanced_pointing
        self.sizes = sizes
        random.shuffle(self.sizes)
        self.elapsed = 0
        self.mouse_moving = False
        self.df = pd.DataFrame(columns=FIELDS)
        print("timestamp (ISO); user_id; advanced_pointing; trial; distance; target_size; time(ms); click_offset_x; click_offset_y")

    def current_target(self):
        if self.elapsed >= len(self.sizes):
            return None
        else:
            return self.sizes[self.elapsed]

    def register_click(self, target_pos, click_pos, originDistance):
        dist = math.sqrt((target_pos[0]-click_pos[0]) * (target_pos[0]-click_pos[0]) +
                         (target_pos[1]-click_pos[1]) * (target_pos[1]-click_pos[1]))
        if dist > self.current_target():
            return False
        else:
            click_offset = (target_pos[0] - click_pos[0],
                            target_pos[1] - click_pos[1])
            self.log_time(self.stop_measurement(),
                          click_offset, originDistance)
            self.elapsed += 1
            return True

    def log_time(self, time, click_offset, originDistance):
        size = self.current_target()
        timestamp = self.timestamp()
        print("%s; %s; %d; %d; %d; %d; %d; %d" % (timestamp, self.user_id,
              self.elapsed, originDistance, size, time, click_offset[0], click_offset[1]))
        self.df = self.df.append({
            "timestamp": timestamp,
            "id": self.user_id,
            "advanced_pointing": self.advanced_pointing,
            "trial": self.elapsed,
            "distance": originDistance,
            "target_size": size,
            "time_in_ms": time,
            "click_offset_x": click_offset[0],
            "click_offset_y": click_offset[1]
        }, ignore_index=True)

    def writeCSV(self):
        self.df = self.df.to_csv(f'./user{self.user_id}.csv', index=False)

    def start_measurement(self):
        if not self.mouse_moving:
            self.timer.start()
            self.mouse_moving = True

    def stop_measurement(self):
        if self.mouse_moving:
            elapsed = self.timer.elapsed()
            self.mouse_moving = False
            return elapsed
        else:
            self.debug("not running")
            return -1

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def debug(self, msg):
        sys.stderr.write(self.timestamp() + ": " + str(msg) + "\n")


class FittsLawTest(QtWidgets.QWidget):

    def __init__(self, model):
        super(FittsLawTest, self).__init__()
        self.model = model
        self.circles = []
        self.pointing = AdvancedPointing(self.circles)
        self.mouse_pos = [400, 400]
        self.initUI()
        self.targetNum = 0

    def initUI(self):
        self.text = "Please click on the target"
        self.setGeometry(0, 0, 1600, 800)
        self.setWindowTitle('Fitts Law Test')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        QtGui.QCursor.setPos(self.mapToGlobal(
            QtCore.QPoint(self.mouse_pos[0], self.mouse_pos[1])))
        self.setMouseTracking(True)
        self.show()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            xTarget = self.circles[self.targetNum]["xPos"]
            yTarget = self.circles[self.targetNum]["yPos"]
            tp = (xTarget, yTarget)
            originDistance = self.__calcDistance(tp, self.mouse_pos)
            hit = self.model.register_click(
                tp, (ev.x(), ev.y()), originDistance)
            if hit:
                self.mouse_pos[0] = ev.x()
                self.mouse_pos[1] = ev.y()
                self.update()

    def mouseMoveEvent(self, ev):
        if (self.model.advanced_pointing == 1):
            self.pointing.filter({"xPos": ev.x(), "yPos": ev.y()})

        self.model.start_measurement()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawBackground(event, qp)
        self.drawText(event, qp)
        self.drawTarget(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Decorative', 32))
        self.text = "%d / %d (%05d ms)" % (self.model.elapsed,
                                           len(self.model.sizes), self.model.timer.elapsed())
        qp.drawText(event.rect(), QtCore.Qt.AlignBottom, self.text)

    def drawBackground(self, event, qp):
        if self.model.mouse_moving:
            qp.setBrush(QtGui.QColor(220, 190, 190))
        else:
            qp.setBrush(QtGui.QColor(200, 200, 200))
        qp.drawRect(event.rect())

    def drawTarget(self, event, qp):
        if self.model.current_target() is not None:
            size = self.model.current_target()
        else:
            self.model.writeCSV()
            sys.stderr.write("no targets left...")
            sys.exit(1)
        self.circles = self.__getCircles(event, size)
        self.pointing = AdvancedPointing(self.circles)
        self.targetNum = random.randint(0, len(self.circles)-1)
        for i, item in enumerate(self.circles):
            if i == self.targetNum:
                qp.setBrush(QtGui.QColor(200, 34, 20))
                qp.setPen(QtGui.QColor(200, 34, 20))
            else:
                qp.setBrush(QtGui.QColor(0, 0, 0))
                qp.setPen(QtGui.QColor(0, 0, 0))
            qp.drawEllipse(item["xPos"], item["yPos"],
                           item["diameter"], item["diameter"])

    def __getCircles(self, event, size):
        circles = []
        window_width = event.rect().width()
        window_height = event.rect().height()
        for x in range(0, window_width, int(window_width/5)):
            xPos = x + random.randint(size/2, int(window_width/5 - size))
            for y in range(0, window_height, int(window_height/2)):
                yPos = y + random.randint(size/2, window_height/2 - size)
                circles.append({
                    "xPos": xPos,
                    "yPos": yPos,
                    "diameter": size
                })
        return circles

    def __calcDistance(self, target_pos, click_pos):
        return math.sqrt((target_pos[0]-click_pos[0]) ** 2 +
                         (target_pos[1]-click_pos[1]) ** 2)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <setup file>\n" % sys.argv[0])
        sys.exit(1)
    model = FittsLawModel(*parse_setup(sys.argv[1]))
    fitts_law_test = FittsLawTest(model)
    sys.exit(app.exec_())


def parse_setup(filename):
    lines = open(filename, "r").readlines()
    if lines[0].startswith("USER:"):
        user_id = lines[0].split(":")[1].strip()
    else:
        print("Error: wrong file format.")
    if lines[1].startswith("WIDTHS:"):
        width_string = lines[1].split(":")[1].strip()
        widths = [int(x) for x in width_string.split(",")]
    else:
        print("Error: wrong file format.")
    if lines[2].startswith("ADVANCED_POINTING:"):
        advancedPointing = int(lines[2].split(":")[1].strip())
    else:
        print("Error: wrong file format.")
    return user_id, widths, advancedPointing


if __name__ == '__main__':
    main()
