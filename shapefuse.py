try:
    from fx import *
    from tools.objectIterator import getObjects
    from tools.objectIterator import ObjectFinder
except:
    print "You are not running from silhouette"

def createShape(pointsList,name="newshape",frame=0.0,closed = True):
    shape = Shape(Shape.Bspline, name)
    keys = pointsList.keys()
    path = shape.createPath(frame)
    path.closed = closed
    ll = pointsList[keys[0]]
    path.points = ll
    return shape

def createUIShape(point,layer,name="newshape",frame=0.0,closed = True):
    node = activeNode()
    session = node.session
    width, height = session.size 
    shape = Shape(Shape.Bspline, name)
    path = shape.createPath(frame)
    path.closed = False
    amount = 0.05
    sizeX = Point3D((amount/height*100), 0)
    sizeY = Point3D(0, (amount/height*100))
    path.points = [(point[0][0]+sizeX,1,1.0),(point[0][0]+sizeY,1,1.0),(point[0][0]-sizeX,1,1.0),(point[0][0]-sizeY,1,1.0),(point[0][0]+sizeX,1,1.0)]
    color = shape.property("outlineColor")        
    color.setValue(Color(1.0,1.0,0.0,1.0))
    layer.property("objects").addObjects([shape])
    return shape


def createUILayer(node):
    session = node.session
    layer = Layer("SHAPE_FUSE_UI")
    layer.visible = True
    node.property("objects").addObjects([layer])
    return layer


def checkUILayer(node,name):
    session = node.session
    rotoNode = session.node(type="RotoNode")
    layers = getObjects(rotoNode.children, types=[Layer])
    exists = False
    if len(layers) > 0:
        for layer in layers:
            if layer.parent.type == "RotoNode":
                if layer.label == name:
                    exists = True
                    target = layer
                    break
                
        if exists == False:
            target = createUILayer(node)
            
    else:
        target = createUILayer(node)
    return target

def cleanupUI(node,name):
    session = node.session
    rotoNode = session.node(type="RotoNode")
    layers = getObjects(rotoNode.children, types=[Layer])
    if len(layers) > 0:
        for layer in layers:
            if layer.label == name:
                delete([layer])
                break
            
def arrangePoints(pointlist, shape):
    """
    animate the points stored on the pointlist. pointlist[time] = positions
    """
    node = activeNode()
    session = node.session

    for time in pointlist.keys():
        pathProp = shape.property("path")
        pathEditor = PropertyEditor(pathProp)    
        #clone and modify clone to keep original shape intact
        copy2 = shape.clone()
        path = copy2.evalPath(time)
        path.points = pointlist[time]
        copy2.setPath(path, time)
        
        pathProp.setValue(path,time)
        pathEditor.execute()
        path = shape.evalPath(time)


def bvfx_shapefuse(trueselection, action="collect"):
    node = activeNode()
    session = node.session
    selected = getObjects(selection())
    if action =="collect":
        beginUndo("Shape Fuse - Add point") 
        if len(selected)>0:
            for shape in selected:
                if shape.selected:
                    if shape.type == "Shape" and viewer.toolName == "Reshape":
                        #=======================================================
                        # bake the point transform
                        #=======================================================
                        for n in shape.selectedPoints():
                            for time in range(int(session.workRange[0]-session.startFrame),int(session.workRange[1]-session.startFrame+1)):
                                copy = shape.clone()
                                if shape.parent.type == "Layer":
                                    path = copy.evalPath(time)
                                    identity = Matrix()
                                    reverseparent = shape.parent.getTransform(time)
                                    offset_matrix = -identity  * reverseparent 
                                    path.transform(offset_matrix)
                                point = copy.evalPath(time).points[n]
                                #===============================================
                                # for now convert other shapes to bsplines
                                #===============================================
                                if shape.shapeType == Shape.Bezier:
                                    point = (point[1],3,1.0)
                                if shape.shapeType == Shape.Xspline:
                                    point = (point[0],1,1.0)
                                #===============================================
                                # each time position holds all the baked points positions for that time
                                #===============================================
                                try:
                                    trueselection[time].append(point)
                                except:
                                    trueselection[time] = [point]
                                #===============================================
                                # store actual frame point for UI 
                                #===============================================
                                if player.frame == time:
                                    pointUI = point
                            userUI = checkUILayer(node,"SHAPE_FUSE_UI")
                            helpershape = createUIShape([pointUI],userUI,"UI_helper"+str(len(trueselection[trueselection.keys()[0]])),session.workRange[0]-session.startFrame)
            keys = trueselection.keys()
            
            if keys != []:
                print "Added", len(shape.selectedPoints()), "point(s) from", shape.label, "  Total points collected so far:", len(trueselection[keys[0]])
            else:
                print "No points selected. Nothing done."   
        else:
            print "No points selected. Nothing done."
        endUndo()
    if action == "build":
        beginUndo("Shape Fuse - Build Shape") 
        keys = trueselection.keys()
        if len(keys) > 0 and len(trueselection[keys[0]]) > 2:
            newshape = createShape(trueselection,"fuseShape",session.workRange[0]-session.startFrame)
            arrangePoints(trueselection,newshape)
            node.property("objects").addObjects([newshape])
            cleanupUI(node,"SHAPE_FUSE_UI")
            select([newshape])
            
        else:
            print "Can't create shapes with less than 2 points, add more points"
        trueselection = {}
        endUndo()
    return trueselection  

