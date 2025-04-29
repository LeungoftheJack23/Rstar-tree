# RTree.py, contains the R*-tree implementation

from .RTreeNode import RTreeNode
from .Rectangle import Rectangle

class RTree:
    def __init__(self, maxChildren=3, method="MBR Area Enlargement"):
        self.root = RTreeNode()
        self.maxChildren = maxChildren
        self.method = method

    def insert(self, point):
        # Treat the point as a rectangle
        rectangle = Rectangle(point[0], point[1], point[0], point[1])
        leaf = self.chooseLeaf(self.root, rectangle)
        leaf.addChild(rectangle)

        # split if children exceed maximum of children
        if len(leaf.children) > self.maxChildren:
            self.splitNode(leaf)

    def chooseLeaf(self, node, rectangle):
        if node.isLeaf:
            return node
        else:
            if self.method == "MBR Area Enlargement":
                bestFit = None
                minAreaIncrease = float('inf')
                for child in node.children:
                    areaIncrease = self.calculateAreaDiff(child.boundingRectangle, rectangle)
                    if areaIncrease < minAreaIncrease:
                        minAreaIncrease = areaIncrease
                        bestFit = child
                return self.chooseLeaf(bestFit, rectangle)
            elif self.method == "MBR Margin Enlargement":
                bestFit = None
                minMarginIncrease = float('inf')
                for child in node.children:
                    marginIncrease = self.calculateMarginDiff(child.boundingRectangle, rectangle)
                    if marginIncrease < minMarginIncrease:
                        minMarginIncrease = marginIncrease
                        bestFit = child
                return self.chooseLeaf(bestFit, rectangle)
            elif self.method == "MBR Overlap Change":
                for child in node.children:
                    if not child.boundingRectangle.isOverlap(rectangle):
                        return self.chooseLeaf(child, rectangle)
                # choose the last child if all MBR are overlapped
                return self.chooseLeaf(child, rectangle)

    def calculateAreaDiff(self, boundingBox, rectangle):
        unionBox = boundingBox.union(rectangle)
        return unionBox.area() - boundingBox.area()

    def calculateMarginDiff(self, boundingBox, rectangle):
        unionBox = boundingBox.union(rectangle)
        return (unionBox.maxX - unionBox.minX) + (unionBox.maxY - unionBox.minY) - ((boundingBox.maxX - boundingBox.minX) + (boundingBox.maxY - boundingBox.minY))

    def splitNode(self, node):
        # split the node into two nodes
        midIndex = len(node.children) // 2
        newNode = RTreeNode(isLeaf=node.isLeaf)
        newNode.children = node.children[midIndex:]
        node.children = node.children[:midIndex]

        node.updateBR()
        newNode.updateBR()

        if node == self.root:
            newRoot = RTreeNode(isLeaf=False)
            newRoot.addChild(node)
            newRoot.addChild(newNode)
            self.root = newRoot
        else:
            parent = self.findParentNode(self.root, node)
            parent.addChild(newNode)
            if len(parent.children) > self.maxChildren:
                self.splitNode(parent)

    def findParentNode(self, current, child):
        if current.isLeaf:
            return None
        for node in current.children:
            if node == child:
                return current
            parent = self.findParentNode(node, child)
            if parent:
                return parent
        return None

    def display(self, node=None, level=0):
        # Display the R-tree structure

        if node is None:
            node = self.root

        lines = []
        indent = "    " * level
        lines.append(f"{indent}{'Leaf' if node.isLeaf else 'Node'}: {node.boundingRectangle}, Children: {len(node.children)}")

        for child in node.children:
            if isinstance(child, Rectangle):
                # Show as a point instead of a rectangle
                point = (child.minX, child.minY)
                lines.append(f"{indent}    Child: {point}")
            else:
                lines.extend(self.display(child, level + 1).splitlines())
        
        return "\n".join(lines)  # Return all lines as a whole big string
