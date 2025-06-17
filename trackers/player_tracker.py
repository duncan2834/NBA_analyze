from ultralytics import YOLO
import supervision as sv
import sys
sys.path.append("../")
from utils import read_stub, save_stub

class PlayerTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
    
    def detect_frames(self, frames):
        batchsize = 20
        detections = []
        for i in range(0, len(frames), batchsize):
            batchframe = frames[i:(i + batchsize)]
            detection = self.model.predict(batchframe, conf=0.75)
            detections += detection
        return detections
            
        
    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None:
            if len(tracks) == len(frames):
                return tracks
        
        detections = self.detect_frames(frames)
        tracks = []
        
        for framenum, detection in enumerate(detections):
            cls_name = detection.names
            cls_name_inv = {}
            
            for key, value in cls_name.items():
                cls_name_inv[value] = key
            
            detection_supervision = sv.Detections.from_ultralytics(detection)
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)
            tracks.append({})
            
            h, w, _ = frames[framenum].shape
            
            for frame_detection in detection_with_tracks:
                x1, y1, x2, y2 = map(int, frame_detection[0].tolist())
                x1 = max(0, min(w - 1, x1))
                x2 = max(0, min(w - 1, x2))
                y1 = max(0, min(h - 1, y1))
                y2 = max(0, min(h - 1, y2))
                bbox = [x1, y1, x2, y2]
                cls_id = frame_detection[3]
                track_id = frame_detection[4]
                
                if cls_id == cls_name_inv['player']:
                    tracks[framenum][track_id] = {'box': bbox}
        save_stub(stub_path, tracks)
        return tracks
            