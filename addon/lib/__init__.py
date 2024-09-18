import os
from ctypes import *
from .data import Parameters, QRParameters, create_string, create_default_QRParameters


class Quadwild():
    def __init__(self, mesh_path: str) -> None:
        # quadpatches_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib_quadpatches.dll')
        # quadwild_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib_quadwild.dll')
        quadpatches_lib_path = 'D:\programming\quadwild-bimdf\\build\Build\\bin\Release\lib_quadpatches.dll'
        quadwild_lib_path = 'D:\programming\quadwild-bimdf\\build\Build\\bin\Release\lib_quadwild.dll'

        self.quadpatches = cdll.LoadLibrary(quadpatches_lib_path)
        self.quadwild = cdll.LoadLibrary(quadwild_lib_path)

        self.quadwild.remeshAndField2.argtypes = [POINTER(Parameters), c_char_p, c_char_p, c_char_p]
        self.quadwild.remeshAndField2.restype = None

        self.quadwild.trace2.argtypes = [c_char_p]
        self.quadwild.trace2.restype = c_bool

        self.quadpatches.quadPatches.argtypes = [c_char_p, POINTER(QRParameters), c_float, c_int]
        self.quadpatches.quadPatches.restype = c_int

        self.mesh_path = mesh_path
        self.mesh_path_without_ext, _ = os.path.splitext(mesh_path)
        self.sharp_path = f'{self.mesh_path_without_ext}_rem.sharp'
        self.field_path = f'{self.mesh_path_without_ext}_rem.rosy'
        self.remeshed_path = f'{self.mesh_path_without_ext}_rem'
        self.traced_path = f'{self.mesh_path_without_ext}_rem_p0.obj'
        self.output_path = f'{self.mesh_path_without_ext}_rem_p0_0_quadrangulation.obj'
        self.output_smoothed_path = f'{self.mesh_path_without_ext}_rem_p0_0_quadrangulation_smooth.obj'


    def remeshAndField(self, params: Parameters) -> None:
        mesh_filename_c = create_string(self.mesh_path)
        sharp_filename_c = create_string(self.sharp_path)
        field_filename_c = create_string(self.field_path)
        self.quadwild.remeshAndField2(byref(params), mesh_filename_c, sharp_filename_c, field_filename_c)

    def trace(self) -> bool:
        filename_prefix_c = create_string(self.remeshed_path)
        ret = self.quadwild.trace2(filename_prefix_c)
        print(ret)
        return ret

    def quadrangulate(self) -> int:
        params = create_default_QRParameters()
        mesh_path_c = self.traced_path.encode()
        scaleFact = 1.0
        fixedChartClusters = 0
        ret = self.quadpatches.quadPatches(mesh_path_c, byref(params), scaleFact, fixedChartClusters)
        print(ret)
        return ret


if __name__ == '__main__':
    qw = Quadwild('example/suzanne.obj')
    qw.remeshAndField()
    qw.trace()
    qw.quadrangulate()
