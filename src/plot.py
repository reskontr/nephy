from __future__ import division

import analysis

import numpy


def setterOnly(func):
    return property(fset=func)

class RegressionPlotter(object):
    def __init__(self, controlMeasurements, xAxis, constants, sdLimit, log=False):
        # Avoid calling _updateXConf and _updateTT multiple times by avoiding
        # calling the setters before setting controlMeasurements.
        self._xAxis = xAxis
        self._constants = constants
        self._sdLimit = sdLimit
        self.controlMeasurements = controlMeasurements
        self.log = log

    @setterOnly
    def controlMeasurements(self, measurements):
        # TODO: This method implies too much knowledge about the Measurement type?
        array = numpy.array(measurements)
        self.mltx = numpy.hstack((numpy.ones((len(array), 1)),
                                  array[:, 1:]))
        self.mlty = array[:, 0]

        self.z = numpy.linalg.inv(self.mltx.T.dot(self.mltx))
        self.a = self.z.dot(self.mltx.T).dot(self.mlty)

        u = self.mltx.dot(self.a)
        self.syx = sum((self.mlty - u) ** 2)
        self.syx /= ((self.mltx.shape[0] - 1) - (self.mltx.shape[1] - 1))

        self._updateXConf()
        self._updateTT()

    @property
    def xAxis(self):
        return self._xAxis

    @xAxis.setter
    def xAxis(self, axis):
        self._xAxis = axis
        self._updateXConf()

    @property
    def constants(self):
        return self._constants

    @constants.setter
    def constants(self, constants):
        self._constants = constants
        self._updateXConf()

    @property
    def sdLimit(self):
        return self._sdLimit

    @sdLimit.setter
    def sdLimit(self, limit):
        self._sdLimit = limit
        self._updateTT()

    def _updateXConf(self):
        xMin = min(self.mltx[:, self.xAxis])
        xMax = max(self.mltx[:, self.xAxis])

        # Build xConf column by column.
        # The first column is just ones.
        self.xConf = numpy.ones((self.mltx.shape[0], 1))
        for i in xrange(1, self.mltx.shape[1]):
            if i == self.xAxis:
                # The column corresponding to the selected x-axis variable contains
                # linearly spaced values from the minimum to the maximum of the
                # variable in the control measurements.
                column = numpy.linspace(xMin, xMax, self.mltx.shape[0])
            else:
                # The other columns are just the corresponding constants entered in
                # the UI.
                column = numpy.repeat(self.constants.pop(0), self.mltx.shape[0])

            # Convert from a 1D array into a column vector and add to xConf.
            column = column.reshape((self.mltx.shape[0], 1))
            self.xConf = numpy.hstack((self.xConf, column))

        # Update aux
        self.aux = self.z.dot(self.xConf.T)

    def _updateTT(self):
        df = (self.mltx.shape[0] - 1) - (self.mltx.shape[1] - 1)
        if df < 20:
            self.tt = self.sdLimit + 2.439 / (df - 1)
        else:
            self.tt = self.sdLimit + 2.439 / df

    def plotAdjustedControlMeasurements(self):
        points = []
        for i, t in enumerate(self.mltx[:, self.xAxis]):
            u = self.mlty[i]

            for j in xrange(1, self.mltx.shape[1]):
                if j != self.xAxis:
                    u += self.a[j] * (self.xConf[i, j] - self.mltx[i, j])

            if self.log:
                u = numpy.exp(u)

            points.append((t, u))

        return sorted(points)

    def plotFittedLine(self):
        points = []
        for i, t in enumerate(self.xConf[:, self.xAxis]):
            u = self.a.dot(self.xConf[i])
            if self.log:
                u = numpy.exp(u)

            points.append((t, u))

        return sorted(points)

    def plotConfidenceLimits(self):
        lowerConfPoints = []
        upperConfPoints = []
        for i, t in enumerate(self.xConf[:, self.xAxis]):
            yConf = self.xConf[i].dot(self.aux.T[i])
            yConf = self.tt * numpy.sqrt(self.syx * yConf)

            u = self.a.dot(self.xConf[i])

            w = u - yConf
            if self.log:
                w = numpy.exp(w)

            lowerConfPoints.append((t, w))

            w = u + yConf
            if self.log:
                w = numpy.exp(w)

            upperConfPoints.append((t, w))

        return sorted(lowerConfPoints), sorted(upperConfPoints)

    def plotPredictionLimits(self):
        lowerPredPoints = []
        upperPredPoints = []
        for i, t in enumerate(self.xConf[:, self.xAxis]):
            yConf = self.xConf[i].dot(self.aux.T[i])
            yPred = 1 + yConf
            yPred = self.tt * numpy.sqrt(self.syx * yPred)

            u = self.a.dot(self.xConf[i])

            w = u + yPred
            if self.log:
                w = numpy.exp(w)

            upperPredPoints.append((t, w))

            w = u - yPred
            if self.log:
                w = numpy.exp(w)

            lowerPredPoints.append((t, w))

        return sorted(lowerPredPoints), sorted(upperPredPoints)
