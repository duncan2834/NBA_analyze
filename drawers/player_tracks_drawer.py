from .utils import draw_ellipse, draw_triangle

class Player_Track_Drawer:
    def __init__(self, team_1_color=(255, 0, 0), team_2_color=(255, 255, 255)):
        self.default_team = 1
        self.team_1_color = team_1_color
        self.team_2_color = team_2_color
    
    def draw(self, video_frames, tracks, player_assignment, ball_control):
        output_video_frames = []
        
        for framenum, frame in enumerate(video_frames):
            frame = frame.copy()
            player_assign_each_frame = player_assignment[framenum]

            player_control_ball = ball_control[framenum]
            
            for track_id, player in tracks[framenum].items():
                bbox = player['box']
                team_id = player_assign_each_frame.get(track_id, self.default_team)
                if team_id == 1:
                    color = self.team_1_color
                else:
                    color = self.team_2_color
                if track_id == player_control_ball:
                    frame = draw_triangle(frame, bbox, (0, 0, 255))
                frame = draw_ellipse(frame, bbox, color, track_id)
            output_video_frames.append(frame)
        return output_video_frames 