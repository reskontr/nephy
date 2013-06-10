from __future__ import division
import collections

import numpy


Measurement = collections.namedtuple("Measurement",
                                     ["measurement",
                                      "age",
                                      "height",
                                      "temperature"])

ReferenceValues = collections.namedtuple("ReferenceValues",
                                         ["pValue",
                                          "tScore",
                                          "estimate",
                                          "lowerLimit",
                                          "upperLimit"])

class AnalysisError(Exception):
    pass

def isOdd(x):
    return bool(x & 1)

def calculateReferenceValues(measurement,
                             age,
                             height,
                             temperature,
                             controlMeasurements,
                             sdLimit,
                             log=False):
    def calculatePValue(df, tScore):
        if df >= 125:
            xx = tScore * (1 - 1 / 4 / df) / numpy.sqrt(1 + tScore * tScore / 2 / df)
            xx = abs(xx) / numpy.sqrt(2)

            aa = numpy.array([0.0705230784,
                              0.0422820123,
                              0.0092705272,
                              0.0001520143,
                              0.0002765672,
                              0.0000430638])
            pValue = 1 + aa.dot(xx**numpy.arange(1, 7))

            if pValue > 0:
                pValue = (1 / pValue)**16

            pValue /= 2

            return pValue

        xx = numpy.arctan(tScore / numpy.sqrt(df))

        if df == 1:
            pValue = 2 * xx / numpy.pi
            pValue = 0.5 - 0.5 * pValue * numpy.sign(tScore)
            return pValue

        if isOdd(df):
            pValue = numpy.cos(xx)
            nb = 2
        else:
            pValue = 1
            nb = 1

        s = pValue
        ne = df - 3
        if ne >= nb:
            for i in xrange(nb, ne + 1, 2):
                pValue *= numpy.cos(xx) ** 2 * i / (i + 1)
                s += pValue

        pValue = numpy.sin(xx) * s
        if isOdd(df):
            pValue = 2 * (xx + pValue) / numpy.pi

        pValue = 0.5 - 0.5 * pValue * numpy.sign(tScore)
        return pValue

    if len(controlMeasurements) < 6:
        raise AnalysisError("need at least 6 control measurements, got {}".format(len(controlMeasurements)))

    controlMeasurementArray = numpy.array(controlMeasurements)
    mltx = numpy.hstack((numpy.ones((len(controlMeasurements), 1)),
                         controlMeasurementArray[:, 1:]))
    mlty = controlMeasurementArray[:, 0]

    if log:
        measurement = numpy.log(measurement)
        mlty = numpy.log(mlty)

    # Linear regression
    z = numpy.linalg.inv(mltx.T.dot(mltx))
    a = z.dot(mltx.T).dot(mlty)

    n = mltx.shape[0] - 1
    m = mltx.shape[1] - 1

    u = mltx.dot(a)
    syx = sum((mlty - u) ** 2)
    syx = syx / (n - m)

    x = [1, age, height, temperature]
    yEst = numpy.inner(a, x)

    df = n - m

    if df < 20:
        tt = sdLimit + 2.439 / (df - 1)
    else:
        tt = sdLimit + 2.439 / df

    sd = 1 + z.dot(x).dot(x)
    sd = numpy.sqrt(syx * sd)

    yPred = tt * sd
    tScore = abs(yEst - measurement) / sd
    pValue = calculatePValue(df, tScore)

    # Two-tailed test
    pValue *= 2

    if log:
        yl = numpy.exp(yEst - yPred)
        yu = numpy.exp(yEst + yPred)
        yEst = numpy.exp(yEst)
    else:
        yl = yEst - yPred
        yu = yEst + yPred

    return ReferenceValues(pValue=pValue,
                           tScore=tScore,
                           estimate=yEst,
                           lowerLimit=yl,
                           upperLimit=yu)
