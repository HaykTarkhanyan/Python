import pyautogui as pg

first_cord =  [198,624]
second_cord = [290,624]
third_cord =  [389,624]
forth_cord =  [481,624]

pixel_color = [51,69,69]

pg.moveTo(second_cord)

# def check_if_same(arr1,arr2):
#     for i,j in zip(arr1,arr2):
#         if i!=j:
#             return False
#     return True

def check_if_near(arr1,arr2):
    
  dist = 0
  for i in range(len(arr1)):
    dist += (arr1[i]-arr2[i])**2
  if dist<1000:
    return True
  return False


tiles = [first_cord, second_cord, third_cord, forth_cord]


for j in range(700):
    for i in range(len(tiles)):
        if check_if_near(pg.pixel(tiles[i][0],tiles[i][1]),pixel_color):
            pg.moveTo(tiles[i][0], tiles[i][1])
            pg.click()
