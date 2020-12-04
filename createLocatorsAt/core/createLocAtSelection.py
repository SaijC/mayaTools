import maya.api.OpenMaya as om2
from createLocatorsAt.utils import utils
reload(utils)

def createLocAtSelection(mObjs, mDagMod):
    """
    create locator at selection
    :param mObjs: MObject
    :param mDagMod: MDagModifier
    :return: None
    """
    for mObj in mObjs:
        mFn = om2.MFnDependencyNode(mObj)
        locMObj = utils.createNode(mDagMod, 'locator', '{}_LOC'.format(mFn.name()))
        locMObjHandle = om2.MObjectHandle(locMObj)

        mMtx = utils.getMtx(locMObjHandle, 'worldMatrix')
        utils.setAtters(locMObjHandle, mMtx)

