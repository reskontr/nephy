import itertools
import nose

import plot
import analysis


def assertPlotsAlmostEqual(plot1, plot2):
    for (x1, y1), (x2, y2) in itertools.izip(plot1, plot2):
        nose.tools.assert_almost_equal(x1, x2)
        nose.tools.assert_almost_equal(y1, y2)

class TestRegressionPlotter(object):
    def setUp(self):
        self.controlMeasurements = [analysis.Measurement(3.6, 25.9, 171, 27.5),
                                    analysis.Measurement(3.0, 33.6, 182, 31.5),
                                    analysis.Measurement(4.0, 23.1, 167, 30.3),
                                    analysis.Measurement(3.3, 22.3, 164, 28.9),
                                    analysis.Measurement(2.9, 27.9, 168, 32.5),
                                    analysis.Measurement(3.6, 29.3, 171, 27.8)]
        self.xAxis = 1
        self.constants = [175, 30]
        self.sdLimit = 2.5

    def testPlotsCorrectAdjustedControlMeasurements(self):
        plotter = plot.RegressionPlotter(self.controlMeasurements,
                                         self.xAxis,
                                         self.constants,
                                         self.sdLimit)
        points = plotter.plotAdjustedControlMeasurements()
        assertPlotsAlmostEqual(points,
                               [(22.3, 3.65304809267073),
                                (23.1, 4.35272518507524),
                                (25.9, 3.54517915614724),
                                (27.9, 3.40383187238366),
                                (29.3, 3.57135086592728),
                                (33.6, 2.84512425801692)])

    def testPlotsCorrectFittedLine(self):
        plotter = plot.RegressionPlotter(self.controlMeasurements,
                                         self.xAxis,
                                         self.constants,
                                         self.sdLimit)
        points = plotter.plotFittedLine()
        assertPlotsAlmostEqual(points,
                               [(22.3,  4.00832674986015),
                                (24.56, 3.79440927933722),
                                (26.82, 3.58049180881429),
                                (29.08, 3.36657433829135),
                                (31.34, 3.15265686776842),
                                (33.6,  2.93873939724549)])

    def testPlotsCorrectConfidenceLimits(self):
        plotter = plot.RegressionPlotter(self.controlMeasurements,
                                         self.xAxis,
                                         self.constants,
                                         self.sdLimit)
        lowerPoints, upperPoints = plotter.plotConfidenceLimits()
        assertPlotsAlmostEqual(lowerPoints,
                               [(22.3,  -0.372754367086868),
                                (24.56,  0.637453602633786),
                                (26.82,  1.57062680652045),
                                (29.08,  2.17769406610401),
                                (31.34,  1.7076634189521),
                                (33.6,   0.476369273965386)])
        assertPlotsAlmostEqual(upperPoints,
                               [(22.3,  8.38940786680718),
                                (24.56, 6.95136495604066),
                                (26.82, 5.59035681110813),
                                (29.08, 4.5554546104787),
                                (31.34, 4.59765031658474),
                                (33.6,  5.40110952052559)])

    def testPlotsCorrectPredictionLimits(self):
        plotter = plot.RegressionPlotter(self.controlMeasurements,
                                         self.xAxis,
                                         self.constants,
                                         self.sdLimit)
        lowerPoints, upperPoints = plotter.plotPredictionLimits()
        assertPlotsAlmostEqual(lowerPoints,
                               [(22.3,  -0.876763866705963),
                                (24.56, -3.13726960846159E-02),
                                (26.82,  0.629255473608618),
                                (29.08,  0.900063669271487),
                                (31.34,  0.552994457778492),
                                (33.6,  -0.337463466255952)])
        assertPlotsAlmostEqual(upperPoints,
                               [(22.3,  8.89341736642627),
                                (24.56,  7.62019125475906),
                                (26.82,  6.53172814401996),
                                (29.08,  5.83308500731122),
                                (31.34,  5.75231927775835),
                                (33.6,  6.21494226074693)])
