import sys
sys.path.append("../")
from utils import measure_distance, get_center_bbox

class Ball_Control:
    def __init__(self):
        self.possession_threshold = 30
        self.min_frame = 8
        self.containment_threshold = 0.95

    def get_keypoint(self, player_bbox, ball_center):
        ball_x, ball_y = ball_center[0], ball_center[1]
        x1, y1, x2, y2 = player_bbox
        w = x2 - x1
        h = y2 - y1
        outputs = []
        if ball_y > y1 and ball_y < y2:
            outputs.append((x1, ball_y))
            outputs.append((x2, ball_y))
        if ball_x > x1 and ball_x < x2:
            outputs.append((ball_x, y1))
            outputs.append((ball_x, y2))
            
        outputs += [
            (x1, y1), # topleft
            (x2, y1), # topright
            (x1, y2), # botleft
            (x2, y2), # botright
            (x1 + w//2, y1), # top_center
            (x1 + w//2, y2), # bot_center
            (x1, y1 + h//2), # left_center
            (x2, y1 + h//2) # right_center
        ]
        return outputs

    def minimum_distance_to_ball(self, player_bbox, ball_center):
        keypoints = self.get_keypoint(player_bbox, ball_center)
        return min(measure_distance(ball_center, keypoint) for keypoint in keypoints)
    
    def contain_ratio(self, player_bbox, ball_bbox): # tinh do overlap cua ball voi player bbox
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox
        
        iou_x1 = max(px1, bx1)
        iou_x2 = min(px2, bx2)
        iou_y1 = max(py1, by1)
        iou_y2 = min(py2, by2)
        
        if iou_x1 > iou_x2 or iou_y1 > iou_y2:
            return 0.0
        
        ball_area = (bx2 - bx1) * (by2 - by1)
        iou = (iou_x2 - iou_x1) * (iou_y2 - iou_y1)
        
        containment_ratio = iou / ball_area
        
        return containment_ratio
    
    def find_best_candidate_possession(self, ball_center, player_tracks_frame, ball_bbox):
        contain_list = []
        min_dist_list = []
        
        for player_id, player_info in player_tracks_frame.items():
            player_bbox = player_info.get('box', [])
            if not player_bbox:
                continue
            
            containment = self.contain_ratio(player_bbox, ball_bbox)
            min_distance = self.minimum_distance_to_ball(player_bbox, ball_center)
            # neu overlap nhieu hon threshold(1st pri)
            if containment > self.containment_threshold:
                contain_list.append((player_id, containment))
            else: # neu gan qua bong nhat (2nd pri)
                min_dist_list.append((player_id, min_distance))
            
            if contain_list:
                max_contain = max(contain_list, key=lambda x: x[1])
                return max_contain[0]
            if min_dist_list:
                min_dist = min(min_dist_list, key=lambda x: x[1])
                if min_dist[1] < self.possession_threshold:
                    return min_dist[0]
            
        return -1 # neu ko th nao thoa man
    
    def detect_ball_possesion(self, player_tracks, ball_tracks):
        num_frames = len(ball_tracks)
        possesion_list = [-1] * num_frames
        consecutive_dict = {}
        
        for frame_num in range(num_frames):
            ball_info = ball_tracks[frame_num].get(1, {})
            if not ball_info:
                continue
            
            ball_bbox = ball_info.get('box', [])
            if not ball_bbox:
                continue
            
            ball_center = get_center_bbox(ball_bbox)
            best_player_id = self.find_best_candidate_possession(ball_center, player_tracks[frame_num], ball_bbox)
            
            if best_player_id != -1:
                num_consecutive_frames = consecutive_dict.get(best_player_id, 0) + 1
                consecutive_dict = {best_player_id: num_consecutive_frames}
                
                if consecutive_dict[best_player_id] >= self.min_frame:
                    possesion_list[frame_num] = best_player_id
            else: # neu ma ko detect th nao control bong
                consecutive_dict = {}
        
        return possesion_list
                    
            
            
            
                
                