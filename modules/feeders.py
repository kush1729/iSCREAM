import locations

class PointIterator(object):
    def __init__(self, line):
        self.line = line

        if self.line.iterate_direction == 1:
            self.location = locations.Point.copy(line.start)
        else:
            self.location = locations.Point.copy(line.end)
        
    def next(self, direction = 1):
        if self.line.is_vertical:
            self.location.y_coordinate += direction * self.line.direction
        elif self.line.is_horizontal:
            self.location.x_coordinate += direction * self.line.direction
        if self.location == self.line.start or self.location == self.line.end:
            raise StopIteration
        return locations.Point.copy(self.location)

class LineFeeder(object):
    def __init__(self, point_list):
        self.point_list = point_list
        self.point_list_len = len(point_list)
        self.current_line_index = 0
    
    def next(self, direction = 1):
        if direction == 1:
            first_point = self.point_list[self.current_line_index]
            second_point = self.point_list[(self.current_line_index + direction) % self.point_list_len]
        else:
            first_point = self.point_list[(self.current_line_index + direction) % self.point_list_len]
            second_point = self.point_list[self.current_line_index]
        
        
        line_to_return = locations.Line(first_point, second_point)
        line_to_return.iterate_direction = direction
        return line_to_return
    
    def change_current_line_index(self, direction):
        self.current_line_index = (self.current_line_index + direction) % self.point_list_len


class PointFeeder(object):
    def __init__(self, point_list):
        self.line_feed = LineFeeder(point_list)
        self.at_vertex = True
    
    def next(self, direction = 1):
        try:
            if self.at_vertex:
                self.current_line = self.line_feed.next(direction)
                self.point_feed = PointIterator(self.current_line)
                self.last_vertex = locations.Point.copy(self.point_feed.location)
                self.at_vertex = False
            
            return self.point_feed.next(direction)
        except StopIteration:
            if self.last_vertex != self.point_feed.location:
                self.line_feed.change_current_line_index(direction)
            self.at_vertex = True
            return locations.Point.copy(self.point_feed.location)

if __name__ == '__main__':
    lf = PointFeeder([locations.Point(0, 0), locations.Point(0, 5), locations.Point(5, 5), locations.Point(5, 0)])
    for i in xrange(3):
        print lf.next(1)
    for i in xrange(10):
        print lf.next(-1)