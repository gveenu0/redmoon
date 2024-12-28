from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
import numpy as np
import os

# Function to add a random frame after every 8th frame
def add_random_frames(video_clip):
    frames = list(video_clip.iter_frames())
    fps = video_clip.fps
    new_frames = []
    for i, frame in enumerate(frames):
        new_frames.append(frame)
        if (i + 1) % 8 == 0:  # After every 8th frame
            # Create a random frame (subtle variation of the current frame)
            random_frame = frame + np.random.randint(-1, 2, frame.shape, dtype='int')
            random_frame = np.clip(random_frame, 0, 255)  # Ensure valid pixel values
            new_frames.append(random_frame.astype('uint8'))
    # Use ImageSequenceClip to create a video from frames
    return ImageSequenceClip(new_frames, fps=fps)

# Function to add subtle noise to the audio
def add_subtle_audio_noise(audio_clip, noise_level=0.001):
    def add_noise(get_frame, t):
        frame = get_frame(t)
        noise = np.random.normal(0, noise_level, frame.shape)  # Add low-level noise
        return np.clip(frame + noise, -1.0, 1.0)  # Ensure valid audio range

    return audio_clip.fl(add_noise)

# Function to apply alterations
def apply_alterations(input_video_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load video and audio
    video_clip = VideoFileClip(input_video_path)
    original_audio = video_clip.audio

    # Add random frames
    video_with_random_frames = add_random_frames(video_clip)

    # Add noise to the audio
    audio_with_noise = add_subtle_audio_noise(original_audio)

    # Combine altered video and audio
    altered_video = video_with_random_frames.set_audio(audio_with_noise)

    # Save the altered video
    altered_video_path = os.path.join(output_folder, "altered_video.mp4")
    altered_video.write_videofile(altered_video_path, codec="libx264", audio_codec="aac")

    print(f"Video with subtle alterations saved at: {altered_video_path}")

# Main function
def main():
    input_video_path = r"C:\Users\Veenu_Gupta\Pictures\Camera Roll\WIN_20230806_19_59_20_Pro.mp4"

    # Replace with your video file path
    output_folder = "altered_video_output"  # Folder to save output
    apply_alterations(input_video_path, output_folder)

if __name__ == "__main__":
    main()
