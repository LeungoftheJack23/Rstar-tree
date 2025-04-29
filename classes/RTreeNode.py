# RTreeNode.py, contains in the R*-tree implementation

class RTreeNode:
    def __init__(self, isLeaf=True):
        self.isLeaf = isLeaf
        self.children = []
        self.boundingRectangle = None

    def addChild(self, child):
        self.children.append(child)
        self.updateBR()

    def updateBR(self):
        if self.children:
            # For leaf nodes, Rectangle objects are the children
            # For non-leaf nodes, RTreeNode objects are the children
            if self.isLeaf:
                self.boundingRectangle = self.children[0]
            else:
                self.boundingRectangle = self.children[0].boundingRectangle
                
            for child in self.children[1:]:
                if self.isLeaf:
                    self.boundingRectangle = self.boundingRectangle.union(child)
                else:
                    self.boundingRectangle = self.boundingRectangle.union(child.boundingRectangle)

    # show if the top is Node/Leaf with the amount of children
    def __repr__(self):
        return f"{'Leaf' if self.isLeaf else 'Node'}: {self.boundingRectangle}, Children: {len(self.children)}"
