import os
from ctypes import *


class Parameters(Structure):
    _fields_ = [
        ('remesh', c_bool),
        ('sharpAngle', c_float),
        ('alpha', c_float),
        ('scaleFact', c_float),
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
        ("ilpMethod", c_int),  # assuming ILPMethod is an enum
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
        ("chartSmoothingIterations", c_int),
        ("quadrangulationFixedSmoothingIterations", c_int),
        ("quadrangulationNonFixedSmoothingIterations", c_int),
        ("doubletRemoval", c_bool),
        ("resultSmoothingIterations", c_int),
        ("resultSmoothingNRing", c_double),
        ("resultSmoothingLaplacianIterations", c_int),
        ("resultSmoothingLaplacianNRing", c_double),
        ("callbackTimeLimit", POINTER(c_float)),
        ("callbackGapLimit", POINTER(c_float)),
    ]


def create_string(input):
    # return input
    return create_string_buffer(str.encode(input, encoding='utf-8'))
    # return create_string_buffer(input)
    # return bytes(input, encoding='utf-8')


def create_default_QRParameters():
    callbackTimeLimitDefault = [8, 3.00, 5.000, 10.0, 20.0, 30.0, 60.0, 90.0, 120.0]
    callbackGapLimitDefault = [8, 0.005, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.3]

    params = QRParameters()
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
    params.scaleFact = 1
    params.fixedChartClusters = 0
    params.useFlowSolver = 1
    params.flow_config_filename = "flow_virtual_simple.json".encode()
    params.satsuma_config_filename = "satsuma_default.json".encode()

    params.chartSmoothingIterations = 0
    params.quadrangulationFixedSmoothingIterations = 0
    params.quadrangulationNonFixedSmoothingIterations = 0
    params.feasibilityFix = False

    return params


class TestStruct(Structure):
    _fields_ = [
        ('stringHello', c_char_p),
        ('stringWorld', c_char_p),
    ]



quadpatches_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib_quadpatches.dll')
quadwild_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib_quadwild.dll')


def main(mesh_filename: str):
    quadpatches = cdll.LoadLibrary(quadpatches_lib_path)
    quadwild = cdll.LoadLibrary(quadwild_lib_path)

    quadwild.remeshAndField2.argtypes = [POINTER(Parameters), c_char_p, c_char_p, c_char_p]
    quadwild.remeshAndField2.restype = None

    quadwild.trace2.argtypes = [c_char_p]
    quadwild.trace2.restype = c_bool

    quadpatches.quadPatches.argtypes = [c_char_p, POINTER(QRParameters), c_float, c_int]
    quadpatches.quadPatches.restype = c_int


    mesh_name, ext = os.path.splitext(mesh_filename)

    params = Parameters(remesh=True, sharpAngle=35, alpha=0.01, scaleFact=1, hasFeature=False, hasField=False)
    mesh_filename_c = create_string(mesh_filename)
    sharp_filename_c = create_string(f'{mesh_name}.sharp')
    field_filename_c = create_string(f'{mesh_name}.rosy')
    quadwild.remeshAndField2(byref(params), mesh_filename_c, sharp_filename_c, field_filename_c)

    filename_prefix_c = create_string(f'{mesh_name}_rem')
    ret = quadwild.trace2(filename_prefix_c)
    print(ret)


    params = create_default_QRParameters()
    mesh_path_c = f'{mesh_name}_rem_p0.obj'.encode()
    scaleFact = 1.0
    fixedChartClusters = 0
    ret = quadpatches.quadPatches(mesh_path_c, byref(params), scaleFact, fixedChartClusters)
    print(ret)

    # print(quadwild.trace2)
    # print(quadwild.remeshAndField2)
    # print(quadpatches.quadrangulate)


if __name__ == '__main__':
    main('example/suzanne.obj')
