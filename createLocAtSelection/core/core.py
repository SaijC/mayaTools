import maya.api.OpenMaya as om2
from createLocAtSelection.utils import utils

def createLocAtSelection():
    selList = om2.MGlobal.getActiveSelectionList()
    mObjs = [selList.getDependNode(idx) for idx in range(selList.length())]
    mDagMod = om2.MDagModifier()

    for mObj in mObjs:
        mObjHandle = om2.MObjectHandle(mObj)
        mFn = om2.MFnDependencyNode(mObj)
        locMObj = utils.createNode("locator", "{}_LOC".format(mFn.name()), mDagMod)
        locMObjHandle = om2.MObjectHandle(locMObj)

        mPlug = utils.findPlug(mObjHandle, "worldMatrix")
        if mPlug.isArray:
            mtxIdxZero = mPlug.elementByLogicalIndex(0)

            plugMObj = mtxIdxZero.asMObject()
            mFnMtxData = om2.MFnMatrixData(plugMObj)
            mMtx = mFnMtxData.matrix()

            utils.setAtters(locMObjHandle, mMtx)

createLocAtSelection()