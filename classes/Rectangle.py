# Rectangle.py, contains in the R*-tree implementation

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
