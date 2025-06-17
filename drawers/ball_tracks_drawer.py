from .utils import draw_triangle

class Ball_Track_Drawer:
    def __init__(self):
        pass
    
    def draw(self, video_frames, tracks):
        output_video_frames = []
        
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            ball_dict = tracks[frame_num]
            for _, ball in ball_dict.items():
                bbox = ball['box']
                if bbox is None:
                    continue
                frame = draw_triangle(frame, bbox, (0, 255, 0))
            output_video_frames.append(frame)
        return output_video_frames