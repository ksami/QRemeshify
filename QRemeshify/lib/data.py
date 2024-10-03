from ctypes import *

class Parameters(Structure):
    _fields_ = [
        ('remesh', c_bool),
        ('sharpAngle', c_float),
        ('alpha', c_float),  # Unused
        ('scaleFact', c_float),  #Unused
        ('hasFeature', c_bool),
        ('hasField', c_bool),
    ]


class QRParameters(Structure):
    _fields_ = [
        ("useFlowSolver", c_bool),
        ("flow_config_filename", c_char_p),
        ("satsuma_config_filename", c_char_p),
        ("initialRemeshing", c_bool),
        ("initialRemeshingEdgeFactor", c_double),
        ("reproject", c_bool),
        ("splitConcaves", c_bool),
        ("finalSmoothing", c_bool),

        ("ilpMethod", c_int),
        ("alpha", c_double),
        ("isometry", c_bool),
        ("regularityQuadrilaterals", c_bool),
        ("regularityNonQuadrilaterals", c_bool),
        ("regularityNonQuadrilateralsWeight", c_double),
        ("alignSingularities", c_bool),
        ("alignSingularitiesWeight", c_double),
        ("repeatLosingConstraintsIterations", c_bool),
        ("repeatLosingConstraintsQuads", c_bool),
        ("repeatLosingConstraintsNonQuads", c_bool),
        ("repeatLosingConstraintsAlign", c_bool),
        ("feasibilityFix", c_bool),
        ("hardParityConstraint", c_bool),

        ("timeLimit", c_double),
        ("gapLimit", c_double),
        ("minimumGap", c_double),
        ("callbackTimeLimit", POINTER(c_float)),
        ("callbackGapLimit", POINTER(c_float)),

        ("chartSmoothingIterations", c_int),
        ("quadrangulationFixedSmoothingIterations", c_int),
        ("quadrangulationNonFixedSmoothingIterations", c_int),
        ("doubletRemoval", c_bool),

        ("resultSmoothingIterations", c_int),
        ("resultSmoothingNRing", c_double),
        ("resultSmoothingLaplacianIterations", c_int),
        ("resultSmoothingLaplacianNRing", c_double),
    ]


def create_string(input):
    return create_string_buffer(str.encode(input, encoding='utf-8'))


def create_default_QRParameters():
    callbackTimeLimitDefault = [3.00, 5.000, 10.0, 20.0, 30.0, 60.0, 90.0, 120.0]
    callbackGapLimitDefault = [0.005, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.3]

    params = QRParameters()

    # Possibly unused
    params.initialRemeshing = True
    params.initialRemeshingEdgeFactor = 1
    params.reproject = True
    params.splitConcaves = False
    params.finalSmoothing = True
    params.doubletRemoval = True
    params.resultSmoothingIterations = 5
    params.resultSmoothingNRing = 3
    params.resultSmoothingLaplacianIterations = 2
    params.resultSmoothingLaplacianNRing = 3

    # From configs
    params.alpha = 0.005
    params.ilpMethod = 1
    params.timeLimit = 200
    params.gapLimit = 0.0
    params.callbackTimeLimit = (c_float * len(callbackTimeLimitDefault))(*callbackTimeLimitDefault)
    params.callbackGapLimit = (c_float * len(callbackGapLimitDefault))(*callbackGapLimitDefault)
    params.minimumGap = 0.4
    params.isometry = 1
    params.regularityQuadrilaterals = 1
    params.regularityNonQuadrilaterals = 1
    params.regularityNonQuadrilateralsWeight = 0.9
    params.alignSingularities = 1
    params.alignSingularitiesWeight = 0.1
    params.repeatLosingConstraintsIterations = 1
    params.repeatLosingConstraintsQuads = 0
    params.repeatLosingConstraintsNonQuads = 0
    params.repeatLosingConstraintsAlign = 1
    params.hardParityConstraint = 1
    params.useFlowSolver = 1
    params.flow_config_filename = "config/main_config/flow_virtual_simple.json".encode()
    params.satsuma_config_filename = "config/satsuma/default.json".encode()

    # Hardcoded in lib
    params.chartSmoothingIterations = 0
    params.quadrangulationFixedSmoothingIterations = 0
    params.quadrangulationNonFixedSmoothingIterations = 0
    params.feasibilityFix = False

    return params
