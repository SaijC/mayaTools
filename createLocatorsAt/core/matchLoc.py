from AL.maya2 import om2
from saveLoadLocator.utils import utils as utils
reload(utils)

def mtachLocatorTransform(applyTranslate, applyRotate, applyScale):
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


        # if locator is selected
        if '_LOC' in selObjMFn.name():
            # use locators worldMatrix and match objects parent inv matrix
            mtx = selObjWMtx * matchObjParentInvMtx
            utils.setSRTAttrs(matchObjHandle, mtx, applyTranslate, applyRotate, applyScale)
        else:
            mtx = matchObjMtx * selObjParentInvMtx
            utils.setSRTAttrs(selObjHandle, mtx, applyTranslate, applyRotate, applyScale)

