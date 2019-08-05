import json
import cv2

import matplotlib.pyplot as plt
import numpy as np

from collections import namedtuple

# for modifing parametrs go to line ~220

Line = namedtuple("Line", ["xmin", "xmax"],  rename=False)
# we will need this namedtuples in the class

Rect_base = namedtuple(
    "Rect_base", ['xminim', 'xmaxim', 'yminim', 'ymaxim'], rename=False)

class Rectangle:
    """
    Rectangle class has methods to understand which rectangle is nested,
    calculate its area, calculate ovelap area, depending on precentage of overlapped
    area can expand one rectangle or cut it. All this staff is done with taking into
    account that one rectangle is more significant then another one.
    """
    def __init__(self, tuple_to_inherit, importance, threshold):
        # rectangle is inintialized only by it's cordinates and importance
        self.xmin = tuple_to_inherit.xminim
        self.ymin = tuple_to_inherit.yminim
        self.xmax = tuple_to_inherit.xmaxim
        self.ymax = tuple_to_inherit.ymaxim

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
        if self.line_croper(self.line_x, other.line_x) == "Already Done" and \
           self.line_croper(self.line_y, other.line_y) == "Already Done":
            # case when they are cross shaped
            new_min_x, new_min_y = max(
                self.xmin, other.xmin), max(self.ymin, other.ymin)
            new_max_x, new_max_y = min(
                self.xmax, other.xmax), min(self.ymax, other.ymax)

            return ("Second rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " +
                    str(new_max_x) + "  " + str(new_max_y),
                    [new_min_x, new_min_y, new_max_x, new_max_y])

        if self.line_croper(self.line_x, other.line_x) == "Already Done":
            # if x axes lines are nested we don't change them
            new_min_y, new_max_y = self.line_croper(self.line_y, other.line_y)
            new_min_x, new_max_x = [other.xmin, other.xmax]
            return ("Second rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " +
                    str(new_max_x) + "  " + str(new_max_y),
                    [new_min_x, new_min_y, new_max_x, new_max_y])

        elif self.line_croper(self.line_y, other.line_y) == "Already Done":
            # if y axes lines are nested we don't change them
            new_min_x, new_max_x = self.line_croper(self.line_x, other.line_x)
            new_min_y, new_max_y = [other.ymin, other.ymax]
            return ("First rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " +
                    str(new_max_x) + "  " + str(new_max_y),
                    [new_min_x, new_min_y, new_max_x, new_max_y])

        else:
            # once it changes horizontal cordinates, once vertiacals and compares
            # which crop caused more area to lose
            new_min_x, new_max_x = self.line_croper(
                self.line_x, other.line_x)
            new_min_y, new_max_y = self.line_croper(
                self.line_y, other.line_y)

            # calculating areas in two different cut types
            area_1 = (new_max_x - new_min_x) * \
                     (other.ymax - other.ymin)
            area_2 = (new_max_y - new_min_y) * \
                     (other.xmax - other.xmin)

            if area_1 < area_2:
                # decide which cut is the best
                return ("Second rectangle's new cordinates are: \n" +
                        "   xmin, ymin: " + str(other.xmin) + "  " + str(new_min_y) +
                        "\n   xmax, ymax: " +
                        str(other.xmax) + "  " + str(new_max_y),
                        [other.xmin, new_min_y, other.xmax, new_max_y])
            else:
                return ("Second rectangle's new cordinates are: \n" +
                        "   xmin, ymin: " + str(new_min_x) + "  " + str(other.xmin) +
                        "\n   xmax, ymax: " +
                        str(new_max_x) + "  " + str(other.xmax),
                        [new_min_x, other.xmin, new_max_x, other.xmax])

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
                    "\n   xmax, ymax: " +
                    str(new_max_x) + "  " + str(new_max_y),
                    [new_min_x, new_min_y, new_max_x, new_max_y])

        # depending of rects importance it changes one of them
        else:
            self.line_x = Line(new_min_x, new_max_x)
            self.line_y = Line(new_min_y, new_max_y)
            return ("First rectangle's new cordinates are: \n" +
                    "   xmin, ymin: " + str(new_min_x) + "  " + str(new_min_y) +
                    "\n   xmax, ymax: " +
                    # added for visualizing
                    str(new_max_x) + "  " + str(new_max_y),
                    [new_min_x, new_min_y, new_max_x, new_max_y])

    def case_classifier(self, other):
        # function checks how big is overlaping part and decide to crop or expand
        # also this fucntions runs function coresponding to classified case
        little_rect = min(self.area, other.area)
        overlap_percentage = self.calculate_overlap_area(other) / little_rect
        if overlap_percentage < self.threshold:
            return self.cropper(other)
        return self.expander(other)

    def visualise(self,other, file_name):
        # drawing with openCV
        image_width = 50*(max(self.xmax, other.xmax) - min(self.xmin, other.xmin)) + 200
        image_height = 50*(max(self.ymax, other.ymax) - min(self.ymin, other.ymin)) + 200


        empty_image = 255 * np.ones(shape = [image_height, image_width, 3])

        cv2.rectangle(empty_image,(50 * self.xmin,50 * self.ymin),
                     (50 * self.xmax,50 * self.ymax),(0,0,255),5)
        cv2.rectangle(empty_image,(50 * other.xmin,50 * other.ymin),
                     (50 * other.xmax,50 * other.ymax),(255,255,0),5)

        cv2.imwrite("{}.png". format(file_name), empty_image)




# threshold helps to understand what to use (cropper or expander)
threshold = 0.7
importance_first = 9
importance_second = 1

rect_named_1 = Rect_base(xminim = 2,  yminim = 2, xmaxim = 6, ymaxim = 6)
rect_named_2 = Rect_base(xminim = 4,  yminim = 3, xmaxim = 8, ymaxim = 8)

re_1 = Rectangle(rect_named_1, importance_first, threshold)
re_2 = Rectangle(rect_named_2, importance_second, threshold)


# code below is for visualizing with matplotlib
# input should be xmin, ymin, width, height
rect = plt.Rectangle((re_1.xmin / 10, re_1.ymin / 10),
                     (re_1.xmax - re_1.xmin) / 10, (re_1.ymax - re_1.ymin) / 10,
                     color='r', alpha=0.9)

rect_2 = plt.Rectangle((re_2.xmin / 10, re_2.ymin / 10),
                       (re_2.xmax - re_2.xmin) /
                       10, (re_2.ymax - re_2.ymin) / 10,
                       color='y', alpha=0.9)

# drawing with openCV
re_1.visualise(re_2, "unchanged")

print(Rectangle.__doc__)

# all the results are shown by code below
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

# check if everything is already done
if (not (re_1.check_if_nested(re_2) == "None of rectangles are nested")) or \
        re_1.calculate_overlap_area(re_2) == 0:
    print("No need to change anything")
else:
    if re_1.importance > re_2.importance:
        re_2.xmin, re_2.ymin, re_2.xmax, re_2.ymax = re_1.case_classifier(re_2)[
            1]
        print(re_1.case_classifier(re_2)[0])
    else:
        re_1.xmin, re_1.ymin, re_1.xmax, re_1.ymax = re_2.case_classifier(re_1)[
            1]

        print(re_2.case_classifier(re_1)[0])


# code below is for visualizing with matplotlib
rect_new = plt.Rectangle((re_1.xmin / 10, re_1.ymin / 10),
                         (re_1.xmax - re_1.xmin) /
                         10, (re_1.ymax - re_1.ymin) / 10,
                         color='r', alpha=1)

rect_new_2 = plt.Rectangle((re_2.xmin / 10, re_2.ymin / 10),
                           (re_2.xmax - re_2.xmin) /
                           10, (re_2.ymax - re_2.ymin) / 10,
                           color='y', alpha=1)


fig = plt.figure()

ax = fig.add_subplot(1, 2, 1)
ax_2 = fig.add_subplot(1, 2, 2)

ax.title.set_text("Before changes")
ax_2.title.set_text("Changed version")

# depending on importance display signifiant is the top
if re_1.importance < re_2.importance:
    ax.add_patch(rect)
    ax.add_patch(rect_2)
else:
    ax.add_patch(rect_2)
    ax.add_patch(rect)

ax_2.add_patch(rect_new)
ax_2.add_patch(rect_new_2)


plt.show()

# drawing with openCV
re_1.visualise(re_2, "after_changes")

# converting to json

Square_to_json = namedtuple("Square", 'xmin ymin xmax ymax')

first_square = Square_to_json(re_1.xmin, re_1.ymin, re_1.xmax, re_1.ymax)
second_square = Square_to_json(re_2.xmin, re_2.ymin, re_2.xmax, re_2.ymax)

first = json.dumps(first_square._asdict(), indent=4)
second = json.dumps(second_square._asdict(), indent=4)


with open('first_square.json', 'w') as json_file:
    json.dump(first, json_file)
with open('second_square.json', 'w') as json_file:
    json.dump(second, json_file)
