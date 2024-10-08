from bpy.types import PropertyGroup
from bpy.props import *


class QWPropertyGroup(PropertyGroup):
    debug:              BoolProperty(name="Debug Mode", description="Show meshes from intermediate steps", default=False)
    useCache:           BoolProperty(name="Use Cache", description="Reuses previously calculated features and only runs quadrangulate step. Must run all steps at least once before enabling this.\n(May be out of sync if mesh has been modified)", default=False)
    enableRemesh:       BoolProperty(name="Preprocess", description="Decimates, triangulates, and tries to fix common geometry issues", default=True)
    enableSmoothing:    BoolProperty(name="Smoothing", description="Performs smoothing after quadrangulation", default=True)
    enableSharp:        BoolProperty(name="Sharp Detection", description="Enable detection of sharp features from edges marked sharp, seams, and from angle threshold", default=True)
    sharpAngle:         FloatProperty(name="Angle Threshold", description="Angle threshold for sharp edges", min=0, soft_min=0.1, max=180, soft_max=179.9, default=35, precision=1, step=10, subtype="UNSIGNED")
    symmetryX:          BoolProperty(name="X", description="Enable symmetry in X-axis", default=False)
    symmetryY:          BoolProperty(name="Y", description="Enable symmetry in Y-axis", default=False)
    symmetryZ:          BoolProperty(name="Z", description="Enable symmetry in Z-axis", default=False)


class QRPropertyGroup(PropertyGroup):

    scaleFact: FloatProperty(
        name="Scale Factor",
        description="Values > 1 for larger quads, < 1 to preserve more detail",
        min=0.01,
        max=10,
        default=1,
        subtype="FACTOR"
    )

    fixedChartClusters: IntProperty(
        name="Fixed Chart Clusters",
        description="Fixed chart clusters",
        min=0,
        default=0
    )

    ### QRParameters ###

    alpha: FloatProperty(
        name="Alpha",
        description="Blends between isometry (alpha) and regularity (1-alpha)",
        default=0.005,
        min=0.0,
        max=0.999,
        precision=3,
        step=0.5,
        subtype="FACTOR"
    )

    ilpMethod: EnumProperty(
        name="ILP Method",
        description="ILP method for solving the ILP problem",
        items=[
            ('LEASTSQUARES', 'Least Squares', 'Use least squares ILP method', 1),
            ('ABS', 'Absolute', 'Use absolute ILP method', 2),
        ],
        default='LEASTSQUARES'
    )

    timeLimit: IntProperty(
        name="Time Limit",
        description="Time limit for optimization in seconds",
        default=200,
        min=1
    )

    gapLimit: FloatProperty(
        name="Gap Limit",
        description="Optimization stops when gap value reaches this limit",
        default=0.0,
        min=0.0
    )

    minimumGap: FloatProperty(
        name="Minimum Gap",
        description="Optimization must reach at least this gap value",
        default=0.4,
        min=0.0
    )

    isometry: BoolProperty(
        name="Isometry",
        description="Enable isometry",
        default=True
    )

    regularityQuadrilaterals: BoolProperty(
        name="Regularity Quadrilaterals",
        description="Enable regularity for quadrilaterals",
        default=True
    )

    regularityNonQuadrilaterals: BoolProperty(
        name="Regularity Non-Quadrilaterals",
        description="Enable regularity for non-quadrilaterals",
        default=True
    )

    regularityNonQuadrilateralsWeight: FloatProperty(
        name="Regularity Non-Quadrilaterals Weight",
        description="Weight for regularity of non-quadrilaterals",
        default=0.9,
        min=0.0,
        max=1.0
    )

    alignSingularities: BoolProperty(
        name="Align Singularities",
        description="Enable singularity alignment",
        default=True
    )

    alignSingularitiesWeight: FloatProperty(
        name="Singularity Alignment Weight",
        description="Weight for singularity alignment",
        default=0.1,
        min=0.0,
        max=1.0
    )

    repeatLosingConstraintsIterations: BoolProperty(
        name="Repeat Losing Constraints Iterations",
        description="Repeat losing constraints for iterations",
        default=True
    )

    repeatLosingConstraintsQuads: BoolProperty(
        name="Repeat Losing Constraints Quadrilaterals",
        description="Repeat losing constraints for quadrilaterals",
        default=False
    )

    repeatLosingConstraintsNonQuads: BoolProperty(
        name="Repeat Losing Constraints Non-Quadrilaterals",
        description="Repeat losing constraints for non-quadrilaterals",
        default=False
    )

    repeatLosingConstraintsAlign: BoolProperty(
        name="Repeat Losing Constraints Alignment",
        description="Repeat losing constraints for alignment",
        default=True
    )

    hardParityConstraint: BoolProperty(
        name="Hard Parity Constraint",
        description="Use hard parity constraint",
        default=True
    )

    flowConfig: EnumProperty(
        name="Flow Config",
        description="Flow config to use",
        items=[
            ("SIMPLE", "Simple", "", 1),
            ("HALF", "Half", "", 2),
        ],
        default="SIMPLE"
    )

    satsumaConfig: EnumProperty(
        name="Satsuma Config",
        description="Satsuma config to use",
        items=[
            ("DEFAULT", "Default", "", 1),
            ("MST", "Approx-MST", "", 2),
            ("ROUND2EVEN", "Approx-Round2Even", "", 3),
            ("SYMMDC", "Approx-Symmdc", "", 4),
            ("EDGETHRU", "Edgethru", "", 5),
            ("LEMON", "Lemon", "", 6),
            ("NODETHRU", "Nodethru", "", 7),
        ],
        default="DEFAULT"
    )

    callbackTimeLimit: FloatVectorProperty(
        name="Callback Time Limit",
        description="Callback time limit",
        size=8,
        default=[3.00, 5.000, 10.0, 20.0, 30.0, 60.0, 90.0, 120.0]
    )

    callbackGapLimit: FloatVectorProperty(
        name="Callback Gap Limit",
        description="Callback gap limit",
        size=8,
        precision=3,
        default=[0.005, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.3]
    )
