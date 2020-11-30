typeDict = {
    "decomposeMatrix": ("inputMatrix", ["outputRotate", "outputTranslate", "outputScale"]),

    "transform": (["rotate", "translate", "scale"], "worldMatrix"),

    "multMatrix": ("matrixIn", "matrixSum"),

    "inverseMatrix": ("inputMatrix", "outputMatrix")
}
