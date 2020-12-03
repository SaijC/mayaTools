import maya.api.OpenMaya as om2
from createLocatorsAt.utils import utils
reload(utils)

selList = om2.MGlobal.getActiveSelectionList()
mObjs = [selList.getDependNode(idx) for idx in range(selList.length())]
mDagMod = om2.MDagModifier()


def createLocAtSelection(mObjs, mDagMod):

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

        transX = mFn.findPlug("translateX", False)
        transY = mFn.findPlug("translateY", False)
        transZ = mFn.findPlug("translateZ", False)
        transX.setFloat(mtx[0])
        transY.setFloat(mtx[1])
        transZ.setFloat(mtx[2])





def createLocAtFace(selList, mDagMod):
    """
    Method to create a locator at face center and align it to it's normal
    :param selList: MSelsctionList
    :param mDagMod: MDagModifier
    :return: None
    """
    iter = om2.MItSelectionList(selList, om2.MFn.kMeshPolygonComponent)
    mObj = selList.getDependNode(0)
    objWorldMtx = utils.getMtx(om2.MObjectHandle(mObj), 'worldMatrix')

    while not iter.isDone():
        dag, mObj = selList.getComponent(0)
        idList = om2.MFnSingleIndexedComponent(mObj)
        idElements = idList.getElements()
        polyIter = om2.MItMeshPolygon(dag, mObj)
        while not polyIter.isDone():
            for id in idElements:
                # Get polygon points
                stuff = polyIter.getArea(id)
                print(id, stuff)
                # loc = utils.createLocator(id, 'n', mDagMod)
                # setAtters(loc, normal)
                # triMPointList, triVtxID = polyIter.getTriangle(0)
                # print("triMPointList, triVtxID", triMPointList, triVtxID)
                # point1 = triMPointList[0]
                # point2 = triMPointList[1]
                # point3 = triMPointList[2]
                # polygonCenterMPoint = polyIter.center(om2.MSpace.kObject)
                #
                # # Convert points to MVectors
                # print('point1.x, point1.y, point1.z', point1.x, point1.y, point1.z)
                # p1Vector = om2.MVector(point1.x, point1.y, point1.z)
                # p2Vector = om2.MVector(point2.x, point2.y, point2.z)
                # p3Vector = om2.MVector(point3.x, point3.y, point3.z)
                #
                # # Find Mid points to aim at
                # p1MidVector = p2Vector - p1Vector
                # p2MidVector = p3Vector - p1Vector
                #
                # vector1 = point3 - point1
                # vector2 = point2 - point1
                #
                # # Cross vectors NOTE: vectors2 is negative to make X axsis aiming "out"
                # normalVector = vector1 ^ -vector2
                #
                # mtx = (
                #     normalVector.x, normalVector.y, normalVector.z, 0,
                #     p1MidVector.x, p1MidVector.y, p1MidVector.z, 0,
                #     p2MidVector.x, p2MidVector.y, p2MidVector.z, 0,
                #     polygonCenterMPoint.x, polygonCenterMPoint.y, polygonCenterMPoint.z, polygonCenterMPoint.w
                # )
                #
                #
                # compositMtx = om2.MMatrix(mtx) * objWorldMtx
                #
                # # Set transform
                # locMObjHandle = utils.createLocator(id, "f", mDagMod)
                # if locMObjHandle.isValid():
                #     utils.setAtters(locMObjHandle, compositMtx)
                polyIter.next()
        iter.next()

componentIDs, typeID = utils.getIDsAndTypes(selList)
if typeID == om2.MFn.kMeshPolygonComponent:
    createLocAtFace(selList, mDagMod)
    print("Done! Face locator/s created and placed!")
else:
    print("Please select an polygon")
