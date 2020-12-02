"""
Author:Fangmin Chen
Version: 0.1

This script is created to make life easier for ppl riggers that do a lot of connections in the Graph Editor.
Its designed to be easiely extended to encompas more node simply adding more node to the typeDict dictionary
in form of: {NODETYPE: (INPUTPLUG, OUTPUTPLUG)}
"""
import sys
if not "C:/tools/mayaTools" in sys.path:
    sys.path.append("C:/tools/mayaTools")

import maya.api.OpenMaya as om2
from connectByType.constants import CONSTANTS as CONST
reload(CONST)

dgMod = om2.MDGModifier()

def getInputOutput(srcMobj, trgMobj):
    """
    Get input based on selected MObjects
    :param srcMobj: MObject
    :param trgMobj: MObject
    :return: None
    """
    srcMFn = om2.MFnDependencyNode(srcMobj)
    trgMFn = om2.MFnDependencyNode(trgMobj)

    srcType = srcMFn.typeName
    trgType = trgMFn.typeName

    srcInputPlugs, srcOutputPlugs = CONST.typeDict[srcType]
    trgInputPlugs, trgOutputPlugs = CONST.typeDict[trgType]
    ioPlugsList = [srcOutputPlugs, trgInputPlugs]
    return tuple(ioPlugsList)


def getMPlugs(mFn, mPlugList):
    """
    get MPlugs from a list
    :param mFn: mFn
    :param mPlugList: list
    :return: list
    """
    if type(mPlugList) == list:

        returnList = list()
        for plug in mPlugList:
            mPlug = mFn.findPlug(plug, False)
            if mPlug.isArray or plug == "worldMatrix":
                returnList.append(mPlug.elementByLogicalIndex(0))
            else:
                returnList.append(mPlug)
        return returnList

    elif type(mPlugList) == tuple:
        returnTuple = list()
        for inputList in mPlugList:
            returnTuple.append([mFn.findPlug(mPlug, False) for mPlug in inputList])
        return tuple(returnTuple)

def connectNodes(srcMobjHandle, trgMobjHandle):
    """
    connect nodes
    :param srcMobjHandle: MObjectHandle
    :param trgMobjHandle: MObjectHandle
    :return: None
    """
    assert srcMobjHandle.isValid() == True, "src MObject not valid"
    assert trgMobjHandle.isValid() == True, "trg MObject not valid"

    srcMobj = srcMobjHandle.object()
    trgMobj = trgMobjHandle.object()

    srcMFn = om2.MFnDependencyNode(srcMobj)
    trgMFn = om2.MFnDependencyNode(trgMobj)

    srcOutputPlugList, trgInputPlugList = getInputOutput(srcMobj, trgMobj)
    srcOutputPlugs = getMPlugs(srcMFn, srcOutputPlugList)
    trgInputPlugs = getMPlugs(trgMFn, trgInputPlugList)


    for srcPlug, trgPlug in zip(srcOutputPlugs, trgInputPlugs):
        dgMod.connect(srcPlug, trgPlug)


selList = om2.MGlobal.getActiveSelectionList()
mobjs = [selList.getDependNode(idx) for idx in range(selList.length())]
srcMFn = om2.MFnDependencyNode(mobjs[0])
srcMobjHandle = om2.MObjectHandle(mobjs[0])
srcType = srcMFn.typeName

for mobj in mobjs[1:]:
    trgMobjHandle = om2.MObjectHandle(mobj)
    connectNodes(srcMobjHandle, trgMobjHandle)
dgMod.doIt()
