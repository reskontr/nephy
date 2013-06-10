import analysis

import random
import nose


def generateControlMeasurement():
    return analysis.Measurement(measurement=round(random.gauss(3.5, 0.37), 1),
                                age=round(random.gauss(26.2, 4.46), 1),
                                height=round(random.gauss(171, 6.82), 0),
                                temperature=round(random.gauss(29.6, 1.50), 1))

def outputVisualBasicCodeForControlMeasurements(measurements):
    for i, m in enumerate(measurements):
        print "mltx({}, 1) = {}".format(i, m.age)
        print "mltx({}, 2) = {}".format(i, m.height)
        print "mltx({}, 3) = {}".format(i, m.temperature)
        print "mlty({}) = {}".format(i, m.measurement)

class TestReferenceValueCalculation(object):
    def setUp(self):
        random.seed(1370865830)
        self.measurement = 3.8
        self.age = 48.2
        self.height = 168
        self.temperature = 30.1
        self.controlMeasurements = [analysis.Measurement(3.6, 25.9, 171, 27.5),
                                    analysis.Measurement(3.0, 33.6, 182, 31.5),
                                    analysis.Measurement(4.0, 23.1, 167, 30.3),
                                    analysis.Measurement(3.3, 22.3, 164, 28.9),
                                    analysis.Measurement(2.9, 27.9, 168, 32.5),
                                    analysis.Measurement(3.6, 29.3, 171, 27.8)]

    def generateControlMeasurements(self, numMeasurements):
        for i in xrange(numMeasurements - len(self.controlMeasurements)):
            self.controlMeasurements.append(generateControlMeasurement())

    def testCalculatesCorrectReferenceValues(self):
        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2.5)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.4382926)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.9601592)
        nose.tools.assert_almost_equal(referenceValues.estimate, 1.26233637652953, 6)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, -11.79125, 5)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 14.31592, 5)

    def testCalculatesCorrectReferenceValuesWithLog(self):
        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2.5,
                                                            log=True)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.4311069, 6)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.9782649, 6)
        nose.tools.assert_almost_equal(referenceValues.estimate, 1.82829182172665, 6)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, 4.548519e-2)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 73.48877, 4)

    def testCalculatesCorrectReferenceValuesWithSDLimit2(self):
        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.4382926)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.9601592)
        nose.tools.assert_almost_equal(referenceValues.estimate, 1.26233637652953, 6)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, -10.46977, 5)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 12.99444, 5)

    def testCalculatesCorrectReferenceValuesWithOddDegreesOfFreedom(self):
        self.controlMeasurements.append(generateControlMeasurement())
        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2.5)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.6093462)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.568702, 6)
        nose.tools.assert_almost_equal(referenceValues.estimate, 2.98923381904503, 6)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, -2.313446, 5)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 8.291913, 6)

    def testCalculatesCorrectReferenceValuesWithManyControlMeasurements(self):
        self.generateControlMeasurements(125)

        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2.5)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.3803202, 5)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.8805259, 6)
        nose.tools.assert_almost_equal(referenceValues.estimate, 3.47987502730234)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, 2.563644, 6)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 4.396106)

    def testCalculatesCorrectReferenceValuesWith125DegreesOfFreedom(self):
        self.generateControlMeasurements(129)

        referenceValues = analysis.calculateReferenceValues(self.measurement,
                                                            self.age,
                                                            self.height,
                                                            self.temperature,
                                                            self.controlMeasurements,
                                                            sdLimit=2.5)

        nose.tools.assert_almost_equal(referenceValues.pValue, 0.3630331, 6)
        nose.tools.assert_almost_equal(referenceValues.tScore, 0.9129422, 6)
        nose.tools.assert_almost_equal(referenceValues.estimate, 3.46855531349356)
        nose.tools.assert_almost_equal(referenceValues.lowerLimit, 2.553844, 6)
        nose.tools.assert_almost_equal(referenceValues.upperLimit, 4.383267, 6)

    @nose.tools.raises(analysis.AnalysisError)
    def testTooFewControlMeasurementsRaisesException(self):
        analysis.calculateReferenceValues(self.measurement,
                                          self.age,
                                          self.height,
                                          self.temperature,
                                          self.controlMeasurements[:5],
                                          sdLimit=2.5)

# TODO:
# *underspecified control measurements (shape[0] < shape[1])
# *log
# *isOdd(df)
# *df > 20
# df >= 125
# -df == 1
