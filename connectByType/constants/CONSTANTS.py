typeDict = {
    'decomposeMatrix': (
        ['inputMatrix'],
        ['outputRotate', 'outputTranslate', 'outputScale']
    ),

    'transform': (
        ['rotate', 'translate', 'scale'],
        ['worldMatrix']
    ),

    'multMatrix': (
        ['matrixIn'],
        ['matrixSum']
    ),

    'addMatrix': (
        ['matrixIn'],
        ['matrixSum']
    ),

    'inverseMatrix': (
        ['inputMatrix'],
        ['outputMatrix']
    ),

    'multiplyDivide': (
        (
            ['input1'], ['input2']
        ),
        ['outputX', 'outputY', 'outputZ']
    )
}
