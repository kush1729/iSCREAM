import feeders

class Point(object):
    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
    
    def __eq__(self, point):
        return point.x_coordinate == self.x_coordinate and point.y_coordinate == self.y_coordinate
    
    def __ne__(self, point):
        return not self == point

    def __repr__(self):
        return 'Point({x}, {y})'.format(x=self.x_coordinate, y=self.y_coordinate)

    def copy(point):
        return Point(point.x_coordinate, point.y_coordinate)

class Line(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.is_vertical = False
        self.is_horizontal = False

        if self.start.x_coordinate == self.end.x_coordinate:
            self.is_vertical = True
            self.direction = cmp(end.y_coordinate, start.y_coordinate)
        elif self.start.y_coordinate == self.end.y_coordinate:
            self.is_horizontal = True
            self.direction = cmp(end.x_coordinate, start.x_coordinate)
    
    def __repr__(self):
        return 'Line({point1}, {point2})'.format(point1=repr(self.start), point2=repr(self.end))