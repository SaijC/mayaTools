typeDict = {
    'decomposeMatrix': (
        'inputMatrix',
        ['outputRotate', 'outputTranslate', 'outputScale']
    ),

    'transform': (
        ['rotate', 'translate', 'scale'],
        'worldMatrix'
    ),

    'multMatrix': (
        'matrixIn',
        'matrixSum'
    ),

    'inverseMatrix': ('inputMatrix', 'outputMatrix'),

    'multiplyDivide': (
        (
            ['input1X', 'input1Y', 'input1Z'], ['input2X', 'input2Y', 'input2Z']
        ),
        ['outputX', 'outputY', 'outputZ']
    )
}
