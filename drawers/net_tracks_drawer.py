import cv2

class NetTracksDrawer:
    def __init__(self):
        pass
    
    def draw(self, frames, net_tracks):
        output_frames = []
        
        for frame_num, frame in enumerate(frames):
            frame_drawn = frame.copy()
            
            net_info = net_tracks[frame_num]
            for _, net in net_info.items():
                net_bbox = net['box']
                if net_bbox is None:
                    continue
                x1, y1, x2, y2 = net_bbox
                cv2.rectangle(frame_drawn, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            output_frames.append(frame_drawn)
        return output_frames
            