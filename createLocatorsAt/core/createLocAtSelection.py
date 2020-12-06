import maya.api.OpenMaya as om2
from createLocatorsAt.utils import utils
reload(utils)

def createLocAtSelection():
    """
    create locator at selection
    :param mObjs: MObject
    :param mDagMod: MDagModifier
    :return: None
    """
    selList = om2.MGlobal.getActiveSelectionList()
    mObjs = [selList.getDependNode(idx) for idx in range(selList.length())]
    mDagMod = om2.MDagModifier()

    if mObjs:
        for mObj in mObjs:
            mFn = om2.MFnDependencyNode(mObj)
            srcMObjHandle = om2.MObjectHandle(mObj)

            locMObj = utils.createNode(mDagMod, 'locator', '{}_LOC'.format(mFn.name()))
            locMObjHandle = om2.MObjectHandle(locMObj)

            mMtx = utils.getMtx(srcMObjHandle, 'worldMatrix')
            utils.setAtters(locMObjHandle, mMtx)
    else:
        utils.createNode(mDagMod, 'locator', 'test', )

    mDagMod.doIt()