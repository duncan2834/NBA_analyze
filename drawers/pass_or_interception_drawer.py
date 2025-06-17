import cv2

class PassOrInterceptionDrawer:
    def __init__(self):
        self.num_pass_1 = 0
        self.num_interception_1 = 0
        self.num_pass_2 = 0
        self.num_interception_2 = 0
    
    def draw(self, video_frames, passes, interceptions):
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame_drawn = self.draw_frame(frame, passes[frame_num], interceptions[frame_num])
            output_video_frames.append(frame_drawn)
        return output_video_frames
    
    def draw_frame(self, frame, pass_frame, interception_frame):
        overlay = frame.copy()
        
        frame_h, frame_w = frame.shape[:2]
        
        rect_x1 = frame_w * 0.1
        rect_y1 = frame_h * 0.72
        rect_x2 = frame_w * 0.45
        rect_y2 = frame_h * 0.84
        
        text_x1 = rect_x1 * 1.03
        text_y1 = rect_y1 * 1.07
        
        if pass_frame == 1:
            self.num_pass_1 += 1
        elif pass_frame == 2:
            self.num_pass_2 += 1
            
        if interception_frame == 1:
            self.num_interception_1 += 1
        elif interception_frame == 2:
            self.num_interception_2 += 1
            
        cv2.rectangle(frame, (int(rect_x1), int(rect_y1)), (int(rect_x2), int(rect_y2)), (255, 255, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        cv2.putText(frame, f"Team 1: Pass: {self.num_pass_1}, Interception: {self.num_interception_1}", (int(text_x1), int(text_y1)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(frame, f"Team 2: Pass: {self.num_pass_2}, Interception: {self.num_interception_2}", (int(text_x1), int(text_y1) + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame