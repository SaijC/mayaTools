import maya.api.OpenMaya as om2
from createLocatorsAt.utils import utils
reload(utils)

def matchLoc(applyTranslate, applyRotate, applyScale):
    selList = om2.MGlobal.getActiveSelectionList()
    mObjs = [selList.getDependNode(idx) for idx in range(selList.length())]

    for mObj in mObjs:
        selObjMFn = om2.MFnDependencyNode(mObj)
        selObjHandle = om2.MObjectHandle(mObj)
        selObjWMtx = utils.getMtx(selObjHandle, 'worldMatrix')
        selObjParentInvMtx = utils.getMtx(selObjHandle, 'parentInverseMatrix')

        matchObjHandle = utils.getMatchObject(selObjHandle)
        matchObjMtx = utils.getMtx(matchObjHandle, 'worldMatrix')
        matchObjParentInvMtx = utils.getMtx(matchObjHandle, 'parentInverseMatrix')

        mtx = matchObjMtx * selObjParentInvMtx
        if '_LOC' in selObjMFn.name():
            mtx = selObjWMtx * matchObjParentInvMtx
            utils.setAtters(matchObjHandle, mtx, applyTranslate, applyRotate, applyScale)
        else:
            utils.setAtters(selObjHandle, mtx, applyTranslate, applyRotate, applyScale)
