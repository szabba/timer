#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore


MILIS_PER_SECOND = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60


class Clock(QtCore.QTimer):

    time_changed = QtCore.pyqtSignal(int, int, int)

    def __init__(self, parent=None):

        super(Clock, self).__init__(parent)

        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.timeout.connect(self.tick)

        self.start(MILIS_PER_SECOND)

    def tick(self):

        self.seconds += 1

        self.fix_params()
        self.print_time()

        self.time_changed.emit(
                self.hours,
                self.minutes,
                self.seconds)


    def fix_params(self):

        extra_minutes = self.seconds / SECONDS_PER_MINUTE
        seconds_left = self.seconds - extra_minutes * SECONDS_PER_MINUTE

        self.seconds = seconds_left
        self.minutes += extra_minutes

        extra_hours = self.minutes / MINUTES_PER_HOUR
        minutes_left = self.minutes - extra_hours * MINUTES_PER_HOUR

        self.minutes = minutes_left
        self.hours += extra_hours

    def print_time(self):

        print '%d:%d:%d' % (
                self.hours,
                self.minutes,
                self.seconds)


class TimerLabel(QtGui.QLabel):
    """A label that displays the time"""

    def __init__(self, clock):

        super(TimerLabel, self).__init__("")

        clock.time_changed.connect(self.update_time)

    def update_time(self, hours, minutes, seconds):

        self.setText("%d:%d:%d" % (
            hours,
            minutes,
            seconds))


class TimerWindow(QtGui.QWidget):
    """A timer window"""

    def __init__(self):

        super(TimerWindow, self).__init__()

        self.clock = Clock(self)

        box = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)

        box.addWidget(TimerLabel(self.clock))

        self.setLayout(box)
        self.setWindowTitle('Timer')
        self.show()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    timer = TimerWindow()

    sys.exit(app.exec_())
