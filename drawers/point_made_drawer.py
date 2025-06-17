import cv2

class PointMadeDrawer:
    def __init__(self):
        self.point_3_team_1 = 0
        self.point_2_team_1 = 0
        self.point_3_team_2 = 0
        self.point_2_team_2 = 0
        self.goal_3_team_1 = 0
        self.goal_2_team_1 = 0
        self.goal_3_team_2 = 0
        self.goal_2_team_2 = 0
    
    def draw(self, video_frames, point_made_team_1, point_made_team_2):
        output_frames = []
        
        for frame_num, frame in enumerate(video_frames):
            frame_drawn = frame.copy()
            frame_drawn = self.draw_frame(frame, point_made_team_1[frame_num], point_made_team_2[frame_num])
            output_frames.append(frame_drawn)
        return output_frames
            

    def draw_frame(self, frame, point_made_team_1, point_made_team_2):
        overlay = frame.copy()
        frame_h, frame_w = frame.shape[:2]
        
        rect_x1 = frame_w * 0.08
        rect_y1 = frame_h * 0.05
        rect_x2 = frame_w * 0.36
        rect_y2 = frame_h * 0.16
        
        text_x1 = frame_w * 0.1
        text_y1 = frame_h * 0.1
        
        if point_made_team_1[0] == '3pt':
            self.point_3_team_1 += 1
            if point_made_team_1[1] == 1: # nem 3 vao
                self.goal_3_team_1 += 1
        elif point_made_team_1[0] == '2pt' or point_made_team_1[0] == 'p':
            self.point_2_team_1 += 1
            if point_made_team_1[1] == 1: # nem 2 vao
                self.goal_2_team_1 += 1
                
        if point_made_team_2[0] == '3pt':
            self.point_3_team_2 += 1
            if point_made_team_2[1] == 1: # nem 3 vao
                self.goal_3_team_2 += 1
        elif point_made_team_2[0] == '2pt' or point_made_team_2[0] == 'p':
            self.point_2_team_2 += 1    
            if point_made_team_2[1] == 1: # nem 2 vao
                self.goal_2_team_2 += 1
        
        cv2.rectangle(frame, (int(rect_x1), int(rect_y1)), (int(rect_x2), int(rect_y2)), (255, 255, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        cv2.putText(frame, f"Team 1: 3pt: {self.goal_3_team_1}/{self.point_3_team_1}, 2pt: {self.goal_2_team_1}/{self.point_2_team_1}", (int(text_x1), int(text_y1)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(frame, f"Team 2: 3pt: {self.goal_3_team_2}/{self.point_3_team_2}, 2pt: {self.goal_2_team_2}/{self.point_2_team_2}", (int(text_x1), int(text_y1) + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)
        return frame
