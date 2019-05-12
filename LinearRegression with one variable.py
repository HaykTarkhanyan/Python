import matplotlib.pyplot as plt
import numpy as np
import random

#x_list = [h for h in input().split()]
#y_list = [j for j in input().split()]

#x = []
#y = []
x = [1,2,3,4]
y = [4,4,4,4]

#unfinished code
def normalize_data(x,y):
  x = sorted(x)
  y = sorted(y)
  normalized_x = []
  normalized_y = []
  mean_x, mean_y = np.mean(x), np.mean(y)
  std_div_x, std_div_y = np.std(x), np.std(y)  
  for i in range(len(x)):
    normalized_x.append((x[i]-mean_x)/std_div_x)
    normalized_y.append((y[i]-mean_y)/std_div_y)
  return normalized_x, normalized_y

#print (normalize_data([3,12,4,21,412,2],[523,423,15,234,623,89]))
  
#Let's input our data 
#for i in range(len(x_list)):
#  x.append(int(x_list[i]))
#  y.append(int(y_list[i]))
def generate_random_points(number_of_points):
  x_axis = [i for i in range(-10,10)]
  y_axis = [j for j in range(-9,8)]
  x_cord = []
  y_cord = []
  for i in range(number_of_points):
    x_cord.append(random.choice(x_axis))
    y_cord.append(random.choice(y_axis))
  return x_cord, y_cord

def make_line(new_line_x,intercept,slope): #makes line with given parameters
  new_line_y = [i*slope + intercept for i in new_line_x]
  plt.plot(new_line_x,new_line_y,color = 'magenta', marker='o')
  return new_line_x, new_line_y

def log_loss(x,y,intercept,slope):
  #count how bad current line fits the data
  new_y_values = [i*slope + intercept for i in x]
  #print (new_y_values)
  #print (y)
  log_loss = 0
  for i in range(len(y)):
    log_loss += (new_y_values[i]-y[i])**2
  return log_loss/(2*len(x))

def gradient_descent(intercept, slope,learning_rate,repetitions):
  #now we start to improve our parametrs to find best line
  log_loss_points = []
  for l in range(repetitions):
  #cost_function = log_loss(x,y,slope,intercept)
    #print (l)
    log_loss_points.append(log_loss(x, y, intercept,slope))
    for i in range(len(x)):
      difference_in_intercept = 0
      difference_in_slope = 0
    
      hypotesis = x[i]*slope + intercept
      # not sure about abs
      difference_in_intercept += hypotesis - y[i]
      difference_in_slope = (hypotesis - y[i]) * x[i]

      new_intercept = intercept - difference_in_intercept * learning_rate / len(x)
      new_slope = slope - difference_in_slope * learning_rate / len(x)

      intercept = new_intercept
      slope = new_slope
  return intercept, slope, log_loss_points


intercept, slope, log_loss_points  = gradient_descent(1,-2,0.001,400)
print ("Best pair of intercept and slope is " + str(intercept) + " and " + str(slope))


figure = plt.figure(figsize = (10,8))

x, y = normalize_data(x,y)


plt.scatter(x,y, marker = '*',color="cyan")
#rand_x, rand_y = generate_random_points(30)
#plt.scatter(rand_x, rand_y, marker = 'o', color="green")

#print (make_line(rand_x,intercept,slope))

#plt.plot(range(len(log_loss_points)), log_loss_points)

#print (range(len(log_loss_points)))
#print (log_loss_points)

plt.savefig("points.png")
#plt.show()


"""print (log_loss([4,5,0,3,2,8],[9,12,1,-3,2,35],0,0))
gf = [9,12,1,-3,2,35]
losss = [k**2 for k in gf]
print (sum(losss)/12)
"""