# readvideo and savevideo function
import cv2

def read_video(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames
    
    
def save_video(output_video_path, output_video_frames):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 30, (output_video_frames[0].shape[1], output_video_frames[0].shape[0])) # file, codec, fps, (w, h)
    for frame in output_video_frames:
        out.write(frame)
    out.release()