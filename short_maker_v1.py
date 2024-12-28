import cv2
import moviepy.editor as mp
from datetime import timedelta


def detect_interesting_frames(video_path, sensitivity=30):
    """Detect interesting scenes in a video."""
    cap = cv2.VideoCapture(video_path)
    interesting_timestamps = []
    prev_frame = None
    frame_count = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_timestamps = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        timestamp = frame_count / fps

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            frame_diff = cv2.absdiff(prev_frame, gray_frame)
            motion = cv2.sumElems(frame_diff)[0] / (frame.shape[0] * frame.shape[1])
            if motion > sensitivity:  # Adjust sensitivity as needed
                interesting_timestamps.append(timestamp)
        prev_frame = gray_frame
        frame_timestamps.append(timestamp)

    cap.release()
    return interesting_timestamps, fps


def crop_to_portrait(input_video, output_video, start_time, duration):
    """Crop video to portrait mode and save a clip."""
    clip = mp.VideoFileClip(input_video).subclip(start_time, start_time + duration)
    width, height = clip.size
    crop_width = int(height * 9 / 16)
    x_center = width // 2
    x_start = max(0, x_center - crop_width // 2)
    x_end = x_start + crop_width

    cropped_clip = clip.crop(x1=x_start, x2=x_end)
    cropped_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")


def main():
    input_video = r"C:\Users\Veenu_Gupta\Downloads\PromptPatternFinalV.mp4"
    sensitivity = 30
    clip_duration = 30  # Seconds
    interesting_timestamps, fps = detect_interesting_frames(input_video, sensitivity)

    # Deduplicate and spread out timestamps
    unique_timestamps = []
    last_time = -clip_duration
    for t in sorted(interesting_timestamps):
        if t - last_time >= clip_duration:
            unique_timestamps.append(t)
            last_time = t

    total_clips = len(unique_timestamps)
    print(f"Found {total_clips} interesting clips to process.")

    for idx, timestamp in enumerate(unique_timestamps):
        output_video = f"output_clip_{idx + 1}.mp4"
        print(f"Creating clip {output_video} from {timestamp:.2f}s...")
        crop_to_portrait(input_video, output_video, timestamp, clip_duration)

        # Show progress percentage
        progress = ((idx + 1) / total_clips) * 100
        print(f"Progress: {progress:.2f}%")


if __name__ == "__main__":
    main()
