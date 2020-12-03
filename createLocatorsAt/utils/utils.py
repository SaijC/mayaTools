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


def geIDsAndTypes(selList):
    """
    Get selected component's ID/s
    :param selList: MSelectionList
    :return: list of int
    """
    __, id = selList.getComponent(0)
    idList = om2.MFnSingleIndexedComponent(id)
    idElement = idList.getElements()
    selType = id.apiType()

    return idElement, selType

def createLocator(name, selType, mDagMod):
    """
    create a locator with vertexID in the name
    :param componentID: str/int
    :param selType: str
    :param mDagMod: MDagModifier
    :return: MObjectHandle
    """
    locLocalScale = 0.1
    mDagPath = om2.MDagPath()
    loc = mDagMod.createNode("locator")
    newName = "{}_{}_LOC".format(selType, name)
    mDagMod.renameNode(loc, newName)

    locMObjHandle = om2.MObjectHandle(loc)
    mDagMod.doIt()

    dagPath = mDagPath.getAPathTo(loc)
    shapeDagPath = dagPath.extendToShape()
    shapeMObj = shapeDagPath.node()
    shapeMFn = om2.MFnDependencyNode(shapeMObj)

    shapeLocalScaleX = shapeMFn.findPlug("localScaleX", False)
    shapeLocalScaleY = shapeMFn.findPlug("localScaleY", False)
    shapeLocalScaleZ = shapeMFn.findPlug("localScaleZ", False)
    shapeLocalScaleX.setFloat(locLocalScale)
    shapeLocalScaleY.setFloat(locLocalScale)
    shapeLocalScaleZ.setFloat(locLocalScale)

    return locMObjHandle

