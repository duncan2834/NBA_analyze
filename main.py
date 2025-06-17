from utils import (read_video, save_video)
from trackers import PlayerTracker, BallTracker, NetTrack
from drawers import Player_Track_Drawer, Ball_Track_Drawer, TeamBallControlDrawer, PassOrInterceptionDrawer, RegionPlayerDrawer, NetTracksDrawer, PointMadeDrawer
from team_assigner import Team_Assigner
from ball_control import Ball_Control
from pass_or_interception import PassOrInterception
from court_detector import CourtDetector
from shoot_region_detector import ShootRegion

def main():
    input_video_path = "input_videos/nice_play.mp4"
    video_frames = read_video(input_video_path)
    
    # xet player
    player_tracker = PlayerTracker(model_path='track.pt')
    player_tracks = player_tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path="stubs/player_track_stubs.pkl")
    
    # xet xem trong vung nao
    court_detector = CourtDetector(model_path='seg.pt')
    player_regions = court_detector.get_region(video_frames, player_tracks, read_from_stub=True, stub_path="stubs/player_regions.pkl")

    # xet ball
    ball_tracker = BallTracker(model_path='track.pt')
    ball_tracks = ball_tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path="stubs/ball_track_stubs.pkl")
    # remove wrong ball detection 
    ball_tracks = ball_tracker.remove_wrong_detection(ball_tracks)
    # interpolate ball tracks
    ball_tracks = ball_tracker.ball_interpolating(ball_tracks)
    
    # xet net
    net_tracker = NetTrack(model_path='track.pt')
    net_tracks = net_tracker.get_net(video_frames, read_from_stub=True, stub_path="stubs/net_track_stubs.pkl")
    
    team_assign = Team_Assigner('dark blue shirt', 'white shirt')
    player_teams = team_assign.get_team_each_frame(video_frames, player_tracks, read_from_stub=True, stub_path="stubs/player_assignment_stubs.pkl")
    
    ball_control = Ball_Control()
    ball_possesion_list = ball_control.detect_ball_possesion(player_tracks, ball_tracks)

    # passes and interception
    pass_or_interception = PassOrInterception()
    passes = pass_or_interception.detect_pass(player_teams, ball_possesion_list)
    interceptions  = pass_or_interception.detect_interception(player_teams, ball_possesion_list)
    
    # shoot
    shoot_region_detector = ShootRegion()
    print(shoot_region_detector.get_shoot_frame(net_tracks, ball_tracks, ball_possesion_list))
    shoot_made_team_1, shoot_made_team_2 = shoot_region_detector.player_shoot_region(net_tracks,
                                                                                     ball_tracks,
                                                                                     ball_possesion_list,
                                                                                     player_regions, 
                                                                                     player_teams)
    print(shoot_made_team_1)
    print(shoot_made_team_2)
    
    # draw
    player_tracks_drawer = Player_Track_Drawer()
    ball_tracks_drawer = Ball_Track_Drawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    pass_or_interception_drawer = PassOrInterceptionDrawer()
    region_player_drawer = RegionPlayerDrawer()
    net_tracks_drawer = NetTracksDrawer()
    point_made_drawer = PointMadeDrawer()
    
    output_video_frames = player_tracks_drawer.draw(video_frames, player_tracks, player_teams, ball_possesion_list)
    output_video_frames = net_tracks_drawer.draw(output_video_frames, net_tracks)
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)
    output_video_frames = team_ball_control_drawer.draw(output_video_frames, player_teams, ball_possesion_list)
    output_video_frames = pass_or_interception_drawer.draw(output_video_frames, passes, interceptions)
    output_video_frames = region_player_drawer.draw(output_video_frames, player_tracks, player_regions)
    output_video_frames = point_made_drawer.draw(output_video_frames, shoot_made_team_1, shoot_made_team_2)
    save_video("output_videos/output_video.avi", output_video_frames) 
    
if __name__ == "__main__":
    main()