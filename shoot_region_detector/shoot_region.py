class ShootRegion:
    def __init__(self):
        self.threshold_frame = 8
        self.threshold_contain = 0.7
        
    """
    Tìm xem thời điểm ném là frame nào
    Thời điểm bóng nằm trong net là frame nào
    Nếu như frame trước bóng thuộc kiểm soát của player, mà frame tiếp theo thuộc net thì là shoot
    """
    # check xem bong thuoc bbox net khong
    # -> need: bbox cua net, bbox cua ball tai frame dang xet
    
    def ball_in_net(self, net_bbox, ball_bbox):
        nx1, ny1, nx2, ny2 = net_bbox
        bx1, by1, bx2, by2 = ball_bbox
        
        iou_x1 = max(nx1, bx1)
        iou_x2 = min(nx2, bx2)
        iou_y1 = max(ny1, by1)
        iou_y2 = min(ny2, by2)
        
        if iou_x1 > iou_x2 or iou_y1 > iou_y2:
            return False
        
        overlap = (iou_x2 - iou_x1) * (iou_y2 - iou_y1)
        ball_area = (bx2 - bx1) * (by2 - by1)
        
        iou = overlap / ball_area
        if iou > self.threshold_contain:
            return True
        return False
    
    def get_shoot_frame(self, net_tracks, ball_tracks, possesion_list):
        num_frames = len(possesion_list)
        shoot_list = [(-1, -1)] * num_frames
        prev_control = -1
        prev_frame = -1
        consecutive_dict = {}
        
        # lấy list th nào cầm bóng ở frame nào: possesion_list
        for frame_num in range(1, len(possesion_list)):
            # ktra frame hien tai thuoc control cua player nao
            if possesion_list[frame_num - 1] != -1:
                prev_frame = frame_num - 1
                prev_control = possesion_list[frame_num - 1]
            
            cur_control = possesion_list[frame_num]
            
            if cur_control == -1 and prev_control != -1: # neu bong dang ko thuoc ai va th control truoc do la player
                # xet xem bong co dang thuoc net khong
                net_info = net_tracks[frame_num].get(1, {})
                if not net_info:
                    continue
                net_bbox = net_info.get('box', [])
                if not net_bbox:
                    continue
                
                ball_info = ball_tracks[frame_num].get(1, {})
                if not ball_info:
                    continue
                ball_bbox = ball_info.get('box', [])
                if not ball_bbox:
                    continue
                
                if self.ball_in_net(net_bbox, ball_bbox): # neu bong trong ro
                    # ktra xem so frame ball trong ro vuot nguong khong
                    num_consecutive_frames = consecutive_dict.get(prev_control, 0) + 1
                    consecutive_dict = {prev_control: num_consecutive_frames}
                    
                    if consecutive_dict[prev_control] >= self.threshold_frame:
                        # suy ra th day shoot vao
                        shoot_list[prev_frame] = (prev_control, 1)
                    else: # < th frame la bong miss
                        shoot_list[prev_frame] = (prev_control, -1)
                else:
                    consecutive_dict = {}
                    
        return shoot_list
    
    # xet xem th nem thuoc vung nao
    def player_shoot_region(self, net_tracks, ball_tracks, possesion_list, player_regions, player_assign):
        shoot_list = self.get_shoot_frame(net_tracks, ball_tracks, possesion_list)
        shoot_made_team_1 = [("", -1)] * len(ball_tracks)
        shoot_made_team_2 = [("", -1)] * len(ball_tracks)
        for frame_num, shoot_player in enumerate(shoot_list):
            if shoot_player[0] != -1:
                region = player_regions[frame_num][shoot_player[0]] # 3pt, p, 2pt
                player_shoot_team = player_assign[frame_num][shoot_player[0]] # team 1 or 2
                if player_shoot_team == 1:
                    shoot_made_team_1[frame_num] = (region, shoot_player[1])
                else:
                    shoot_made_team_2[frame_num] = (region, shoot_player[1])
        return shoot_made_team_1, shoot_made_team_2        
                