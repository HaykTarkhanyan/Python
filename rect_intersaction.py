import json
from collections import namedtuple

Line = namedtuple("Line", ["xmin", "xmax"],  rename=False)
# we will need this namedtuple in the class

# for modifing parametrs go to line 150


class Rectangle:
    # rectangle is inintialized only by it's cordinates and importance
    def __init__(self, xmin, ymin, xmax, ymax, importance, threshold):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.importance = importance
        self.threshold = threshold
        # we instanciate rectangle to vertical line and horizantal
        self.line_x = Line(self.xmin, self.xmax)
        self.line_y = Line(self.ymin, self.ymax)
        # area of the rectangle
        self.area = self.calculate_area()

    @staticmethod
    def calculate_two_lines_overlap(line_1, line_2):
        # this static method calculates how much two lines overlap
        overlap_size = min(line_1.xmax, line_2.xmax) - \
            max(line_1.xmin, line_2.xmin)
        # we return difference between minimal value of max. cordinates and
        # maximal value of min. cordinates
        if overlap_size < 0:
            return 0
        return min(line_1.xmax, line_2.xmax) - max(line_1.xmin, line_2.xmin)

    @staticmethod
    def check_if_line_nested(line_1, line_2):
        # checks if second line is in first
        if line_2.xmin > line_1.xmin and line_2.xmax < line_1.xmax:
            return True
        # checks if first line is in second
        if line_1.xmin > line_2.xmin and line_1.xmax < line_2.xmax:
            return True

    @staticmethod
    def line_expander(line_1, line_2):
        # functions returns expanded line we will use it in expander function
        return [min(line_1.xmin, line_2.xmin), max(line_1.xmax, line_2.xmax)]

    def line_croper(self, line_1, line_2):
        # functions returns croped line we will use it in croper function
        # assumes that  line_1 is important
        if self.check_if_line_nested(line_1, line_2):
            return "Already Done"
        # checks if less imporant line is from left or right
        if line_2.xmin > line_1.xmin:
            return [line_1.xmax, line_2.xmax]
        else:
            return [line_2.xmin, line_1.xmin]

    def calculate_area(self):
        # fuction calculates area of the rectangle
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def calculate_overlap_area(self, other):
        # uses defined above function once for each axes individually
        return self.calculate_two_lines_overlap(self.line_x, other.line_x) *  \
            self.calculate_two_lines_overlap(self.line_y, other.line_y)

    def check_if_nested(self, other):
        # checks if one rectangle is in another and specifies which one is which
        if self.calculate_overlap_area(other) == self.area:
            return "First is nested in second"
        # it does it by looking which rectangles area is equal to overlap area
        if self.calculate_overlap_area(other) == other.area:
            return "Second is nested in first"
        return 'None of rectangles are nested'

    def cropper(self, other):
        # this function crops less important rectangle to avoid overlaps
        # also minimizes croped area
        if self.line_croper(self.line_x, other.line_x) == "Already Done":
            # if x axes lines are nested we don't change them
            new_min_y, new_max_y = self.line_croper(self.line_y, other.line_y)
            new_min_x, new_max_x = [other.xmin, other.xmax]
            return ("Second rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " + str(new_max_x) + "  " + str(new_max_y))

        elif self.line_croper(self.line_y, other.line_y) == "Already Done":
            # if y axes lines are nested we don't change them
            new_min_x, new_max_x = self.line_croper(self.line_x, other.line_x)
            new_min_y, new_max_y = [other.ymin, other.ymax]
            return ("First rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " + str(new_max_x) + "  " + str(new_max_y))

        else:
            # once it changes horizontal cordinates, once vertiacals and compares
            # which crop caused more area to lose
            new_min_x, new_max_x = self.line_croper(
                self.line_x, other.line_x)
            new_min_y, new_max_y = self.line_croper(
                self.line_y, other.line_y)

            area_1 = (new_max_x - new_min_x) * \
                     (other.ymax - other.ymin)
            area_2 = (new_max_y - new_min_y) * \
                     (other.xmax - other.xmin)

            if area_1 < area_2:
                return ("Second rectangle's new cordinates are: \n" +
                        "   xmin, ymin: " + str(other.xmin) + "  " + str(new_min_y) +
                        "\n   xmax, ymax: " + str(other.xmax) + "  " + str(new_max_y))
            else:
                return ("Second rectangle's new cordinates are: \n" +
                        "   xmin, ymin: " + str(new_min_x) + "  " + str(other.xmin) +
                        "\n   xmax, ymax: " + str(new_max_x) + "  " + str(other.xmax))

    def expander(self, other):
        # this functions expands less important rectangle so that imported
        # will become nested in it
        new_min_x, new_max_x = self.line_expander(self.line_x, other.line_x)
        new_min_y, new_max_y = self.line_expander(self.line_y, other.line_y)
        # we update x axes vals and y's seperately
        if self.importance > other.importance:
            other.line_x = Line(new_min_x, new_max_x)
            other.line_y = Line(new_min_y, new_max_y)
            return ("Second rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " + str(new_max_x) + "  " + str(new_max_y))

        # depending of rects importance it changes one of them
        else:
            self.line_x = Line(new_min_x, new_max_x)
            self.line_y = Line(new_min_y, new_max_y)
            return ("First rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " + str(new_max_x) + "  " + str(new_max_y))

    def case_classifier(self, other):
        # function checks how big is overlaping part and decide to crop or expand
        # also this fucntions runs function coresponding to classified case
        little_rect = min(self.area, other.area)
        overlap_percentage = self.calculate_overlap_area(other) / little_rect
        if overlap_percentage < self.threshold:
            return self.cropper(other)
        return self.expander(other)


# threshold helps to understand what to use (cropper or expander)
threshold = 0.5
importance_first = 8
importance_second = 6
# re_1 = Rectangle(2, 5, 6, 8, importance_first, threshold)
# re_2 = Rectangle(4, 2, 8, 6, importance_second, threshold)

re_1 = Rectangle(2, 5, 6, 8, importance_first, threshold)
re_2 = Rectangle(4, 2, 5, 6, importance_second, threshold)

print("First rectangle's cordinates are: \n" +
      "   xmin, ymin: " + str(re_1.xmin) + "  " + str(re_1.ymin) +
      "\n   xmax, ymax: " + str(re_1.xmax) + "  " + str(re_1.ymax))
print("Second rectangle's cordinates are: \n" +
      "   xmin, ymin: " + str(re_2.xmin) + "  " + str(re_2.ymin) +
      "\n   xmax, ymax: " + str(re_2.xmax) + "  " + str(re_2.ymax))

print()

print("First rectangle's area is: " + str(re_1.area))
print("Second rectangle's area is: " + str(re_2.area))
print()
print("Overlap area is: " + str(re_1.calculate_overlap_area(re_2)))
print(re_1.check_if_nested(re_2))
print()

if not (re_1.check_if_nested(re_2) == "None of rectangles are nested"):
    print("No need to change anything")
else:
    if re_1.importance > re_2.importance:
        print(re_1.case_classifier(re_2))
    else:
        print(re_2.case_classifier(re_1))


# print(vars(re_2))

# converting to json

Square_to_json = namedtuple("Square", 'xmin ymin xmax ymax')

first_square = Square_to_json(re_1.xmin, re_1.ymin, re_1.xmax, re_1.ymax)
second_square = Square_to_json(re_2.xmin, re_2.ymin, re_2.xmax, re_2.ymax)

first = json.dumps(first_square._asdict(), indent=4)
second = json.dumps(second_square._asdict(), indent=4)

# print(first)
