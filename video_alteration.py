import os
from moviepy.editor import VideoFileClip, AudioFileClip, vfx

# Helper function to speed up audio
def speed_up_audio(audio_clip, factor):
    """Speeds up the audio clip by a given factor."""
    return audio_clip.set_fps(audio_clip.fps * factor)

def subtly_modify_video_and_audio(input_video_path, output_folder):
    # Load video and audio
    clip = VideoFileClip(input_video_path)
    original_audio = clip.audio

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Subtle Video Alterations
    # 1. Slight Color Adjustment
    subtly_color_adjusted = clip.fx(vfx.colorx, 1.05)  # Slightly increase brightness
    subtly_color_adjusted.write_videofile(os.path.join(output_folder, "subtle_color_adjustment.mp4"))

    # 2. Minor Aspect Ratio Change with Padding
    # Resize height and add padding to maintain valid aspect ratio
    target_height = int(clip.h * 0.98)
    padded_clip = clip.resize(height=target_height).margin(top=(clip.h - target_height) // 2, bottom=(clip.h - target_height) // 2, color=(0, 0, 0))
    padded_clip.write_videofile(os.path.join(output_folder, "subtle_aspect_ratio_change.mp4"))

    # 3. Micro Rotation
    subtly_rotated = clip.rotate(1)  # Rotate by 1 degree
    subtly_rotated.write_videofile(os.path.join(output_folder, "subtle_rotation.mp4"))

    # Subtle Audio Alterations
    # 1. Slight Speed Change (Time Stretch)
    subtly_sped_up_audio = speed_up_audio(original_audio, 1.01)  # Speed up by 1%
    subtly_sped_up_clip = clip.set_audio(subtly_sped_up_audio)
    subtly_sped_up_clip.write_videofile(os.path.join(output_folder, "subtle_audio_speedup.mp4"))

    # 2. Volume Adjustment
    subtly_volume_adjusted = original_audio.volumex(0.98)  # Reduce volume by 2%
    subtly_volume_adjusted_clip = clip.set_audio(subtly_volume_adjusted)
    subtly_volume_adjusted_clip.write_videofile(os.path.join(output_folder, "subtle_volume_adjustment.mp4"))

    print(f"Subtle video and audio modifications completed. Check the folder: '{output_folder}'.")

# Main function
def main():
    # Input video file path
    input_video_path = r"C:\Users\Veenu_Gupta\Pictures\Camera Roll\WIN_20230806_19_59_20_Pro.mp4"  # Replace with your video file path

    # Output folder
    output_folder = "subtle_modifications_output"

    # Apply subtle modifications
    subtly_modify_video_and_audio(input_video_path, output_folder)

if __name__ == "__main__":
    main()
