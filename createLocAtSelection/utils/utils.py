import maya.api.OpenMaya as om2

def setAtters(mObjectHandle, mtx):
    """
    Sets translation/rotation
    :param mObjectHandle: MObjectHandle
    :param mtx: MMatrix
    :return: None
    """
    if mObjectHandle.isValid():
        mObj = mObjectHandle.object()
        mFn = om2.MFnDependencyNode(mObj)
        mTransMtx = om2.MTransformationMatrix(mtx)

        trans = mTransMtx.translation(om2.MSpace.kWorld)
        rot = mTransMtx.rotation()
        scl = mTransMtx.scale(om2.MSpace.kObject)

        transX = mFn.findPlug("translateX", False)
        transY = mFn.findPlug("translateY", False)
        transZ = mFn.findPlug("translateZ", False)
        transX.setFloat(trans.x)
        transY.setFloat(trans.y)
        transZ.setFloat(trans.z)

        rotX = mFn.findPlug("rotateX", False)
        rotY = mFn.findPlug("rotateY", False)
        rotZ = mFn.findPlug("rotateZ", False)
        rotX.setFloat(rot.x)
        rotY.setFloat(rot.y)
        rotZ.setFloat(rot.z)

        rotX = mFn.findPlug("scaleX", False)
        rotY = mFn.findPlug("scaleY", False)
        rotZ = mFn.findPlug("scaleZ", False)
        rotX.setFloat(scl[0])
        rotY.setFloat(scl[1])
        rotZ.setFloat(scl[2])


def findPlug(mObjectHandle, searchPlug):
    """
    Creates and names the created node
    :param mObjectHandle: MObjectHandle
    :param findPlug: str
    :return: MPlug
    """
    if mObjectHandle.isValid():
        mObj = mObjectHandle.object()
        mFn = om2.MFnDependencyNode(mObj)
        mPlugs = mFn.findPlug(searchPlug, False)
        return mPlugs


def createNode(nodeTypeName, nodeName, mDagMod):
    """
    Creates and names the created node
    :param nodeTypeName: str
    :param nodeName: str
    :param mDagMod: MDagModifier
    :return: MObjectHandle
    """
    nodeMObj = mDagMod.createNode(nodeTypeName)
    mDagMod.renameNode(nodeMObj, nodeName)
    nodeMObjHandle = om2.MObjectHandle(nodeMObj)
    mDagMod.doIt()

    return nodeMObjHandle