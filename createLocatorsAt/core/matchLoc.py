import maya.api.OpenMaya as om2
from createLocatorsAt.utils import utils

selList = om2.MGlobal.getActiveSelectionList()
mObjs = [selList.getDependNode(idx) for idx in range(selList.length())]

for mObj in mObjs:
    toBeMatchObj = mObj
    toBeMatchObjMFn = om2.MFnDependencyNode(toBeMatchObj)
    toBeMatchObjMobjHandle = om2.MObjectHandle(toBeMatchObj)
    toBeMatchObjMtx = utils.getMtx(toBeMatchObjMobjHandle, 'worldMatrix')
    toBeMatchObjParentInvMtx = utils.getMtx(toBeMatchObjMobjHandle, 'parentInverseMatrix')

    matchToObjHandle = utils.getMatchLocator(toBeMatchObjMobjHandle)
    matchToObjMtx = utils.getMtx(matchToObjHandle)

    print('toBeMatchObjMtx:', toBeMatchObjMtx)
    print('toBeMatchObjParentInvMtx:', toBeMatchObjParentInvMtx)
    print('matchToObjMtx:', matchToObjMtx)

