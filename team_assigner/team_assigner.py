from PIL import Image
import cv2
from transformers import CLIPProcessor, CLIPModel
import sys
sys.path.append('../')
from utils import read_stub, save_stub
class Team_Assigner:
    def __init__(self, team_1_class_name, team_2_class_name):
        self.team_1 = team_1_class_name
        self.team_2 = team_2_class_name
        self.player_team = {}
        
    def load_model(self):
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
        
    def get_player_color(self, frame, bbox):
        image = frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]
        if image.size == 0:
            print(f"bbox: {bbox}")
            
        classes = [self.team_1, self.team_2]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        
        inputs = self.processor(text=classes, images=pil_image, return_tensors='pt', padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        class_name = classes[probs.argmax(dim=1)[0]] # lay th class co prob cao nhat
        return class_name
    
    def get_player_team(self, frame, bbox, player_id):
        if player_id in self.player_team:
            return self.player_team[player_id]
        team_id = 2
        if self.get_player_color(frame, bbox) == self.team_1:
            team_id = 1
        self.player_team[player_id] = team_id
        return team_id
    
    def get_team_each_frame(self, video_frames, tracks, read_from_stub=False, stub_path=None):
        player_assignment = read_stub(read_from_stub, stub_path)
        
        if player_assignment is not None:
            if len(player_assignment) == len(video_frames): # ton tai roi thi return
                return player_assignment
        
        self.load_model()
        player_assignment = []
        for frame_num, detections in enumerate(tracks):
            player_assignment.append({})
            
            if frame_num % 50 == 0:
                self.player_team = {} # reset lai moi khi dc 50frame tranh sai sot
                
            for player_id, track in detections.items():
                team = self.get_player_team(video_frames[frame_num], track['box'], player_id)
                player_assignment[frame_num][player_id] = team
        save_stub(stub_path, player_assignment)
        return player_assignment
                
        