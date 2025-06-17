import cv2
import sys
sys.path.append("../")
from utils import get_center_bbox


class RegionPlayerDrawer:
    def __init__(self):
        pass
    
    def draw(self, video_frames, player_tracks, player_regions):
        outputs_frame = []
        
        for frame_num, frame in enumerate(video_frames):
            frame_drawn = frame.copy()
            
            for player_id, player_info in player_tracks[frame_num].items():
                # lay center cua player
                player_bbox = player_info.get('box', [])
                center_x, center_y = get_center_bbox(player_bbox)
                
                # lay region cua player
                player_region = player_regions[frame_num].get(player_id, -1)
                if player_region == -1:
                    continue
                
                cv2.rectangle(frame_drawn, (center_x - 10, center_y - 10), (center_x + 25, center_y + 10), (0, 0, 0), cv2.FILLED)
                cv2.putText(frame_drawn, f"{player_region}", (center_x - 5, center_y + 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 2)
                
            outputs_frame.append(frame_drawn)
        return outputs_frame
                
                

                