from fx import *
from tools.objectIterator import getObjects
from tools.objectIterator import ObjectFinder
import shapefuse
import sys

class bvfx_ShapeFuse(Action):
    """Create new shapes based on point selections"""

    def __init__(self):
        Action.__init__(self, "BoundaryVFX|Shape Fuse")
        #=======================================================================
        # this pointlist is kept here to be able to keep the points in order over time
        #=======================================================================
        self.pointlist = {}


    def available(self):
        node = activeNode()
        session = activeSession()
        assert session, "Select a Session"
        rotoNode = session.node(type="RotoNode")
        assert rotoNode, "The session does not contain a Roto Node"
        shapes = getObjects(selection())
        assert len(shapes) > 0, "There must be one or more selected shapes/layers"
 
    def execute(self, action="collect"):
        print "\n**********************\nbvfx_ShapeFuse v1.0\nBy Magno Borgo\nBoundaryVFX\n**********************"
        reload(shapefuse)
#         beginUndo("Shape Fuse") 
        self.pointlist = shapefuse.bvfx_shapefuse(self.pointlist,action)
#         endUndo()

addAction(bvfx_ShapeFuse())
