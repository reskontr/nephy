from __future__ import division
import collections

import numpy


Patient = collections.namedtuple("Patient",
                                 ["age",
                                  "height",
                                  "temperature",
                                  "measurement"])

ReferenceValues = collections.namedtuple("ReferenceValues",
                                         ["pvalue",
                                          "tscore",
                                          "estimate",
                                          "lower_limit",
                                          "upper_limit"])

def is_odd(x):
    return bool(x & 1)

def calculate_reference_values(measurement,
                               age,
                               height,
                               temperature,
                               control_patients,
                               sd_limit,
                               log=False):
    def calculate_pvalue(df, tscore):
        if df >= 125:
            xx = tscore * (1 - 1 / 4 / df) / numpy.sqrt(1 + tscore * tscore / 2 / df)
            xx = abs(xx) / numpy.sqrt(2)

            aa = [0.0705230784,
                  0.0422820123,
                  0.0092705272,
                  0.0001520143,
                  0.0002765672,
                  0.0000430638]
            pvalue = 1 + aa * xx**numpy.arange(1, 7)

            if pvalue > 0:
                pvalue = (1 / pvalue)**16

            return pvalue

        xx = numpy.arctan(tscore / numpy.sqrt(df))

        if df == 1:
            pvalue = 2 * xx / numpy.pi
            pvalue = 0.5 - 0.5 * pvalue * numpy.sign(tscore)
            return pvalue

        if is_odd(df):
            pvalue = numpy.cos(xx)
            nb = 2
        else:
            pvalue = 1
            nb = 1

        s = pvalue
        ne = df - 3
        if ne >= nb:
            for i in xrange(nb, ne + 1, 2):
                pvalue *= numpy.cos(xx) ** 2
                s += pvalue

        pvalue = numpy.sin(xx) * s
        if is_odd(df):
            pvalue = 2 * (xx + pvalue) / numpy.pi

        pvalue = 0.5 - 0.5 * pvalue * numpy.sign(tscore)
        return pvalue

    control_patient_array = numpy.array(control_patients)
    mltx = numpy.hstack((numpy.ones((len(control_patients), 1)),
                         control_patient_array[:, :-1]))
    mlty = control_patient_array[:, -1]

    if mltx.shape[0] < mltx.shape[1]:
        # TODO: Raise exception?
        return

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
    y_est = numpy.inner(a, x)

    df = n - m

    if df < 20:
        tt = sd_limit + 2.439 / (df - 1)
    else:
        tt = sd_limit + 2.439 / df

    sd = 1 + z.dot(x).dot(x)
    sd = numpy.sqrt(syx * sd)

    y_pred = tt * sd
    tscore = abs(y_est - measurement) / sd
    pvalue = calculate_pvalue(df, tscore)

    # Two-tailed test
    pvalue *= 2

    if log:
        yl = numpy.exp(y_est - y_pred)
        yu = numpy.exp(y_est + y_pred)
        y_est = numpy.exp(y_est)
    else:
        yl = y_est - y_pred
        yu = y_est + y_pred

    return ReferenceValues(pvalue=pvalue,
                           tscore=tscore,
                           estimate=y_est,
                           lower_limit=yl,
                           upper_limit=yu)
