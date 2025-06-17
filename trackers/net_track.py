from ultralytics import YOLO
import supervision as sv
import sys
sys.path.append("../")
from utils import read_stub, save_stub

class NetTrack:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def detect_frames(self, video_frames):
        detections = []
        batchsize = 20
        for i in range(0, len(video_frames), batchsize):
            batch_frames = video_frames[i: i +batchsize]
            batch_detection = self.model.predict(batch_frames, conf=0.3)
            detections += batch_detection
        return detections
    
    def get_net(self, video_frames, read_from_stub=False, stub_path=None):
        net_tracks = read_stub(read_from_stub, stub_path)
        if net_tracks is not None:
            if len(net_tracks) == len(video_frames):
                return net_tracks
            
        net_tracks = []
        detections = self.detect_frames(video_frames)
        
        for frame_num, detection_frame in enumerate(detections):
            cls_name = detection_frame.names
            cls_name_inv = {v:k for k,v in cls_name.items()}
            
            net_tracks.append({})
            
            detection_frame_sv = sv.Detections.from_ultralytics(detection_frame)
            for detection in detection_frame_sv: # bbox, mask, conf, cls_id, track_id, 
                cls_id = detection[3]
                bbox = detection[0].tolist()
                if cls_id == cls_name_inv['net']:  
                    net_tracks[frame_num][1] = {'box': bbox}
                    
        save_stub(stub_path, net_tracks)
                    
        return net_tracks
                