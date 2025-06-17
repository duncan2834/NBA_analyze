import cv2
import numpy as np
import sys
sys.path.append("../")
from utils import get_bbox_width, get_center_bbox

def draw_triangle(frame, bbox, color):
    x1, y1, x2, y2 = bbox
    x_center, y_center = get_center_bbox(bbox)
    
    triangle_point = np.array([
        [x_center, int(y1)],
        [x_center - 10, int(y1) - 20],
        [x_center + 10, int(y1) - 20]
    ])
    cv2.drawContours(frame, [triangle_point], 0, color, cv2.FILLED)
    cv2.drawContours(frame, [triangle_point], 0, (0, 0, 0), 2)
    
    return frame
    
def draw_ellipse(frame, bbox, color, track_id=None):
    x1, y1, x2, y2 = bbox
    x_center, y_center = get_center_bbox(bbox)
    width = get_bbox_width(bbox)
    # ve hinh ellipse duoi chan player
    cv2.ellipse(frame, 
                center=(x_center, int(y2)), 
                axes=(int(width), int(width*0.35)),
                angle=0,
                startAngle=-25,
                endAngle=235,
                color=color,
                thickness=2,
                lineType=cv2.LINE_4)
    
    # ve them track id cho player
    rect_width = 40
    rect_height = 20
    
    x1_rect = x_center - rect_width//2
    x2_rect = x_center + rect_width//2
    y1_rect = (y2 - rect_height//2) + 15
    y2_rect = (y2 + rect_height//2) + 15
    
    if track_id is not None:
        cv2.rectangle(frame, (int(x1_rect), int(y1_rect)), (int(x2_rect), int(y2_rect)), color, cv2.FILLED)
        x1_text = x1_rect + 12
        if track_id > 99:
            x1_text -= 10
        cv2.putText(frame, str(track_id), (int(x1_text), int(y1_rect) + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
    return frame
    