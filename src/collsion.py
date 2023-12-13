
from math import sqrt


    
def detect_collision(rect_1, rect_2):

    for r1, r2 in [(rect_1, rect_2), (rect_2, rect_1)]:
       
        return point_in_rectangle(r1.topleft, r2) or point_in_rectangle(r1.topright, r2) or \
        point_in_rectangle(r1.bottomright, r2) or point_in_rectangle(r1.bottomleft, r2)
            




def point_in_rectangle(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom
   
    
 