# Rstar-tree.py, contains the R*-tree implementation and a test case

import random

class Rectangle:
    def __init__(self, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

    # returns the Minimum bounding rectangle (MBR) area
    def area(self):
        return (self.maxX - self.minX) * (self.maxY - self.minY)

    # checks if the rectangle overlaps with each other rectangles
    def isOverlap(self, other):
        return not ((self.maxX < other.minX or self.minX > other.maxX) or (self.maxY < other.minY or self.minY > other.maxY))

    # expand the MBR
    def union(self, other):
        return Rectangle(min(self.minX, other.minX), min(self.minY, other.minY), max(self.maxX, other.maxX), max(self.maxY, other.maxY))

    # show rectangle position
    def __repr__(self):
        return f"Rectangle({self.minX}, {self.minY}, {self.maxX}, {self.maxY})"


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


class RTree:
    def __init__(self, maxChildren=3):
        self.root = RTreeNode()
        self.maxChildren = maxChildren

    def insert(self, point):
        rectangle = Rectangle(point[0], point[1], point[0], point[1])  # Create a rectangle for the point
        leaf = self.chooseLeaf(self.root, rectangle)
        leaf.addChild(rectangle)

        # split if children exceed maximum of children
        if len(leaf.children) > self.maxChildren:
            self.splitNode(leaf)

    def chooseLeaf(self, node, rectangle):
        if node.isLeaf:
            return node
        else:
            best_fit = None
            min_area_increase = float('inf')
            for child in node.children:
                area_increase = self.calculateAreaDiff(child.boundingRectangle, rectangle)
                if area_increase < min_area_increase:
                    min_area_increase = area_increase
                    best_fit = child
            return self.chooseLeaf(best_fit, rectangle)

    def calculateAreaDiff(self, bounding_box, rectangle):
        union_box = bounding_box.union(rectangle)
        return union_box.area() - bounding_box.area()

    def splitNode(self, node):
        # split the node into two nodes
        mid_index = len(node.children) // 2
        new_node = RTreeNode(isLeaf=node.isLeaf)
        new_node.children = node.children[mid_index:]
        node.children = node.children[:mid_index]

        node.updateBR()
        new_node.updateBR()

        if node == self.root:
            new_root = RTreeNode(isLeaf=False)
            new_root.addChild(node)
            new_root.addChild(new_node)
            self.root = new_root
        else:
            parent = self.findParentNode(self.root, node)
            parent.addChild(new_node)
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

    def search(self, rectangle):
        return self.searchNode(self.root, rectangle)

    def searchNode(self, node, rectangle):
        if node.isLeaf:
            return [child for child in node.children if child.isOverlap(rectangle)]
        else:
            results = []
            for child in node.children:
                if child.boundingRectangle.isOverlap(rectangle):
                    results.extend(self.searchNode(child, rectangle))
            return results

    def display(self, node=None, level=0):
        """Display the R-tree structure."""
        if node is None:
            node = self.root
        indent = "    " * level
        print(f"{indent}{'Leaf' if node.isLeaf else 'Node'}: {node.boundingRectangle}, Children: {len(node.children)}")
        for child in node.children:
            if isinstance(child, Rectangle):
                print(f"{indent}    Child: {child}")
            else:
                self.display(child, level + 1)


# test
if __name__ == "__main__":
    rtree = RTree(maxChildren=3)
    
    # generate 200 unique random points
    points_set = set()
    while len(points_set) < 5:
        x = round(random.uniform(0, 10), 2)  # round to 2 d.p.
        y = round(random.uniform(0, 10), 2)
        points_set.add((x, y))

    points = list(points_set)
    points = [(3.8, 1.61), (6.77, 1.26), (1.21, 9.89), (8.19, 6.58), (7.48, 6.61), (6.47, 1.5), (4.12, 8.45), (8.87, 8.75), (1.69, 8.67), (7.62, 2.41)]
    print(points)

    for point in points:
        rtree.insert(point)

        # Display the R-tree structure
        print("R-tree structure:")
        rtree.display()
        print("")