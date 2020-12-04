import maya.api.OpenMaya as om2


def setAtters(mObjectHandle, mtx,
              applyTrans=True,
              applyRot=True,
              applyScale=True):
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

        if applyTrans:
            transRootMplug = mFn.findPlug('translate', False)
            transX = transRootMplug.child(0)
            transY = transRootMplug.child(1)
            transZ = transRootMplug.child(2)

            trans = mTransMtx.translation(om2.MSpace.kWorld)
            transX.setFloat(trans.x)
            transY.setFloat(trans.y)
            transZ.setFloat(trans.z)

        if applyRot:
            rotRootMplug = mFn.findPlug('rotate', False)
            rotX = rotRootMplug.child(0)
            rotY = rotRootMplug.child(1)
            rotZ = rotRootMplug.child(2)

            rot = mTransMtx.rotation()
            rotX.setFloat(rot.x)
            rotY.setFloat(rot.y)
            rotZ.setFloat(rot.z)

        if applyScale:
            scl = mTransMtx.scale(om2.MSpace.kObject)
            sclX = mFn.findPlug('scaleX', False)
            sclY = mFn.findPlug('scaleY', False)
            sclZ = mFn.findPlug('scaleZ', False)
            sclX.setFloat(scl[0])
            sclY.setFloat(scl[1])
            sclZ.setFloat(scl[2])


def createNode(mDagMod, nodeTypeName, nodeName=""):
    """
    Creates and names the created node
    :param nodeTypeName: str
    :param nodeName: str
    :param mDagMod: MDagModifier
    :return: MObjectHandle
    """
    nodeMObj = mDagMod.createNode(nodeTypeName)
    if nodeName:
        mDagMod.renameNode(nodeMObj, nodeName)
    nodeMObjHandle = om2.MObjectHandle(nodeMObj)
    mDagMod.doIt()

    return nodeMObjHandle


def getIDsAndTypes(selList):
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
    loc = mDagMod.createNode('locator')
    newName = '{}_{}_LOC'.format(selType, name)
    mDagMod.renameNode(loc, newName)

    locMObjHandle = om2.MObjectHandle(loc)
    mDagMod.doIt()

    dagPath = mDagPath.getAPathTo(loc)
    shapeDagPath = dagPath.extendToShape()
    shapeMObj = shapeDagPath.node()
    shapeMFn = om2.MFnDependencyNode(shapeMObj)

    shapeLocalScaleX = shapeMFn.findPlug('localScaleX', False)
    shapeLocalScaleY = shapeMFn.findPlug('localScaleY', False)
    shapeLocalScaleZ = shapeMFn.findPlug('localScaleZ', False)

    shapeLocalScaleX.setFloat(locLocalScale)
    shapeLocalScaleY.setFloat(locLocalScale)
    shapeLocalScaleZ.setFloat(locLocalScale)

    return locMObjHandle


def getMtx(mObjectHandle, mtxName):
    """
    Get given matrix
    :param mObjectHandle: MObjectHandle
    :param mtxName: str
    :return: MMatrix
    """
    if mObjectHandle.isValid():
        mObj = mObjectHandle.object()
        mFn = om2.MFnDependencyNode(mObj)
        mtxPlug = mFn.findPlug(mtxName, False)
        if mtxPlug.isArray:
            mtxPlug = mtxPlug.elementByLogicalIndex(0)
        plugMObj = mtxPlug.asMObject()

        mFnMtxData = om2.MFnMatrixData(plugMObj)
        mtx = mFnMtxData.matrix()
        return mtx
