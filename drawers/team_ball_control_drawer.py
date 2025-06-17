import numpy as np
import cv2

class TeamBallControlDrawer:
    def __init__(self):
        pass
    
    def get_team_ball_control(self, player_assignment, ball_control):
        team_control = []
        for player_assignment_frame, ball_control_frame in zip(player_assignment, ball_control):
            # neu ko detect duoc ball control(tuc la =-1)
            if ball_control_frame == -1:
                team_control.append(-1)
                continue
            
            # neu th player dc detect la dang cam bong ma ko xuat hien trong phan detect player
            if ball_control_frame not in player_assignment_frame:
                team_control.append(-1)
                continue
            
            # chia team
            if player_assignment_frame[ball_control_frame] == 1:
                team_control.append(1)
            else:
                team_control.append(2)
        
        team_control = np.array(team_control)
        return team_control
    
    def draw(self, video_frames, player_assignment, ball_control):
        team_control = self.get_team_ball_control(player_assignment, ball_control)
        output_video = []
        for frame_num, frame in enumerate(video_frames):
            if frame_num == 0:
                continue
            frame_drawn = self.draw_frame(frame_num, frame, team_control)
            output_video.append(frame_drawn)
        return output_video
            
        
    def draw_frame(self, frame_num, frame, team_control):
        # ve hinh chu nhat overlay
        overlay = frame.copy()
        frame_h, frame_w = overlay.shape[:2] 
        
        rect_x1 = frame_w * 0.6
        rect_y1 = frame_h * 0.72
        rect_x2 = frame_w * 0.9
        rect_y2 = frame_h * 0.8
        
        text_x1 = rect_x1 * 1.03
        text_y1 = rect_y1 * 1.07
        
        cv2.rectangle(frame, (int(rect_x1), int(rect_y1)), (int(rect_x2), int(rect_y2)), (255, 255, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        team_ball_control_till_frame = team_control[: frame_num + 1]
        team_1_control = team_ball_control_till_frame[team_ball_control_till_frame == 1].shape[0]
        team_2_control = team_ball_control_till_frame[team_ball_control_till_frame == 2].shape[0]
        no_control = team_ball_control_till_frame[team_ball_control_till_frame != -1].shape[0]
        if no_control == 0:
            no_control += 1
        team_1_control_per = team_1_control/no_control
        team_2_control_per = team_2_control/no_control
        
        cv2.putText(frame, f"Team 1 Ball Control: {team_1_control_per*100:.2f}%", (int(text_x1), int(text_y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(frame, f"Team 2 Ball Control: {team_2_control_per*100:.2f}%", (int(text_x1), int(text_y1) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return frame
        
