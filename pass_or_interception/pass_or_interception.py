class PassOrInterception:
    def __init__(self):
        pass
    
    def detect_pass(self, player_assignment, ball_control):
        passes = [-1] * len(ball_control)
        prev_control = -1
        prev_frame = -1
        
        for frame_num in range(1, len(ball_control)):
            if ball_control[frame_num - 1] != -1:
                prev_control = ball_control[frame_num - 1]
                prev_frame = frame_num - 1
            
            cur_control = ball_control[frame_num]
            
            if cur_control != prev_control and cur_control != -1 and prev_control != -1:
                cur_team_control = player_assignment[frame_num].get(cur_control, -1)
                prev_team_control = player_assignment[prev_frame].get(prev_control, -1)
                
                if cur_team_control == prev_team_control and prev_team_control != -1:
                    passes[frame_num] = prev_team_control
                    
        return passes
    
    def detect_interception(self, player_assignment, ball_control): # th team nay chuyen cho th team kia
        interceptions = [-1] * len(ball_control)
        prev_control = -1
        prev_frame = -1
        
        for frame_num in range(1, len(ball_control)):
            if ball_control[frame_num - 1] != -1:
                prev_control = ball_control[frame_num - 1]
                prev_frame = frame_num - 1
            
            cur_control = ball_control[frame_num]
            
            if cur_control != prev_control and cur_control != -1 and prev_control != -1:
                cur_team_control = player_assignment[frame_num].get(cur_control, -1)
                prev_team_control = player_assignment[prev_frame].get(prev_control, -1)
                
                if cur_team_control != prev_team_control and prev_team_control != -1 and cur_team_control != -1:
                    interceptions[frame_num] = prev_team_control
                    
        return interceptions
                