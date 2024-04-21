"""
plotting module of the nmraspecds package.
"""
import aspecd.plotting


class SinglePlotter1D(aspecd.plotting.SinglePlotter1D):
    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"


class SinglePlotter2D(aspecd.plotting.SinglePlotter2D):
    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"


class SinglePlotter2DStacked(aspecd.plotting.SinglePlotter2DStacked):
    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"


class MultiPlotter1D(aspecd.plotting.MultiPlotter1D):
    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"


class MultiPlotter1DStacked(aspecd.plotting.MultiPlotter1DStacked):
    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"
