from ultralytics import YOLO
import supervision as sv
import sys
sys.path.append("../")
from utils import read_stub, save_stub
import cv2
import numpy as np

# dung segmentation
class CourtDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        
    def detect_frames(self, video_frames):
        detections = []
        batchsize = 20
        for i in range(0, len(video_frames), batchsize):
            batch = video_frames[i: i+batchsize]
            batch_detections = self.model.predict(batch, conf=0.7)
            detections += batch_detections
                
        return detections
    
    def get_region(self, video_frames, player_tracks, read_from_stub=False, stub_path=None):
        regions = read_stub(read_from_stub, stub_path)
        if regions is not None:
            if len(regions) == len(video_frames):
                return regions
        regions = []
        court_detections = self.detect_frames(video_frames)
        
        for frame_num, (player_info, court_detections_frame) in enumerate(zip(player_tracks, court_detections)):
            regions.append({})
            for player_id, player_bbox_dict in player_info.items():
                # xet xem th dang xet dang thuoc region nao
                court_detections_frame_sv = sv.Detections.from_ultralytics(court_detections_frame)
                
                cls_name = ['3pt', 'p', '2pt']
                # lay foot cua player dang xet
                player_bbox = player_bbox_dict.get('box', [])
                x1, y1, x2, y2 = player_bbox
                center_x = int((x1 + x2)/2)
                center_foot = (center_x, int(y2))
                
                for court_detection_frame in court_detections_frame_sv:
                    cls_id = court_detection_frame[3]
                    mask_frame = court_detection_frame[1]
                    inside = self.mask_analyze(mask_frame, center_foot)
                    if inside == 1:
                        regions[frame_num][player_id] = cls_name[cls_id]
                        break
                    
        save_stub(stub_path, regions)
        return regions            
                    
    def mask_analyze(self, mask_frame, center_foot):
        binary_mask = mask_frame.astype(np.uint8) # chuyen false/True -> 0/1
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # tim duong vien tren binary mask
        # cv2.RETR_EXTERNAL: chi lay contour ngoai cung
        
        if contours:
            contours_max = max(contours, key=cv2.contourArea)
        
        inside = cv2.pointPolygonTest(contours_max, center_foot, measureDist=False)
        """
        measureDist=False: Trả về:

        +1 nếu điểm nằm bên trong polygon.

        0 nếu nằm trên viền.

        -1 nếu nằm ngoài polygon.
        """
        return inside
        
