import supervision as sv
from ultralytics import YOLO
import numpy as np
import pandas as pd
import sys
sys.path.append("../")
from utils import read_stub, save_stub

class BallTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        
    def detect_frames(self, frames):
        batchsize = 20
        detections = []
        for i in range(0, len(frames), batchsize):
            batch_frame = frames[i: (i + batchsize)]
            batch_detection = self.model.predict(batch_frame, conf=0.3)
            detections += batch_detection
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None:
            if len(tracks) == len(frames):
                return tracks
        detections = self.detect_frames(frames)
        tracks = []
        
        for frame_num, detection in enumerate(detections):
            
            detection_supervision = sv.Detections.from_ultralytics(detection)
            tracks.append({})
            cls_names = detection.names
            cls_name_inv = {}
            for key, value in cls_names.items():
                cls_name_inv[value] = key
                
            max_conf = 0
            chosen_box = None
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                conf = frame_detection[2]
                
                if cls_id == cls_name_inv['ball']:
                    if conf > max_conf:
                        max_conf = conf
                        chosen_box = bbox
            if chosen_box is not None:    
                tracks[frame_num][1] = {'box': chosen_box}
        save_stub(stub_path, tracks)
        return tracks
    
    def remove_wrong_detection(self, ball_pos):
        maximum_allowed_distance = 25
        last_good_frame = -1
        
        for i in range(len(ball_pos)):
            cur_bbox = ball_pos[i].get(1, {}).get('box', [])
            if len(cur_bbox) == 0:
                continue
            
            # neu la frame detect dau tien
            if last_good_frame == -1:
                last_good_frame = i
                continue
            
            last_good_box = ball_pos[last_good_frame].get(1, {}).get('box', [])
            frame_gap = i - last_good_frame
            maximum_adjust_distance = maximum_allowed_distance * frame_gap
            
            if np.linalg.norm(np.array(last_good_box[:2]) - np.array(cur_bbox[:2])) > maximum_adjust_distance:
                ball_pos[i] = {}
            else:
                last_good_frame = i
        return ball_pos      
    
    def ball_interpolating(self, ball_pos):
        ball_positions = [x.get(1, {}).get('box', []) for x in ball_pos]
        df = pd.DataFrame(ball_positions, columns=["x1", "y1", "x2", "y2"])
        
        df = df.interpolate()
        df = df.bfill()
        
        ball_positions = [{1: {'box': x}} for x in df.to_numpy().tolist()]
        return ball_positions