import maya.api.OpenMaya as om2
import maya.cmds as cmds


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
            sclRootMplug = mFn.findPlug('scale', False)
            sclX = sclRootMplug.child(0)
            sclY = sclRootMplug.child(1)
            sclZ = sclRootMplug.child(2)

            scl = mTransMtx.scale(om2.MSpace.kObject)
            sclX.setFloat(scl[0])
            sclY.setFloat(scl[1])
            sclZ.setFloat(scl[2])


def createNode(mDagMod, nodeTypeName, nodeName=''):
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

def getMatchObject(mObjHandle):
    if mObjHandle.isValid():
        locSelList = om2.MSelectionList()
        mObj = mObjHandle.object()
        mFn = om2.MFnDependencyNode(mObj)
        objName = mFn.name()
        # if locator selected then find the corresponding match obj
        if '_LOC' in objName:
            objName = objName.replace('_LOC', '')
            # check if pasted in the name
            if '__' in objName:
                objName = objName.split('__')[-1]
        else:
            objName = '{}_LOC'.format(objName)
            # check if pasted in the name
            if cmds.objExists('pasted__{}'.format(objName)):
                objName = 'pasted__{}'.format(objName)

        locSelList.add(objName)
        locMobj = locSelList.getDependNode(0)
        objMobjHandle = om2.MObjectHandle(locMobj)

        return objMobjHandle

def getName(mObjHandle):
    if mObjHandle.isValid():
        mObj = mObjHandle.object()
        mFn = om2.MFnDependencyNode(mObj)
        objName = mFn.name()
        return objName