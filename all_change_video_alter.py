import os
import random

import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from moviepy.audio.fx import all as afx

def speed_up_audio(audio, factor):
    return audio.fx(afx.speedx, factor)

def pixel_shift(frame, t):
    """ Helper function for pixel shifting that accepts frame and time """
    # Create a copy of the frame to avoid modifying a read-only array
    frame = np.copy(frame)

    # Shift a random subset of pixels in the frame
    height, width, _ = frame.shape
    x = random.randint(0, height - 1)
    y = random.randint(0, width - 1)
    shift = random.randint(-2, 2)

    # Get the current pixel value
    original_value = frame[x, y].astype(np.int32)
    # Perform the addition with clamping
    new_value = np.clip(original_value + shift, 0, 255)
    frame[x, y] = new_value.astype(frame.dtype)
    return frame

def apply_alterations(input_video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip(input_video_path)
    original_audio = clip.audio

    # 1. Frame Rate Adjustment (Slightly increase the frame rate)
    altered_frame_rate = clip.set_fps(30.01)  # Slight frame rate increase (imperceptible to human)
    altered_frame_rate_path = os.path.join(output_folder, "altered_frame_rate.mp4")

    # 2. Keyframe Interval Adjustment (Re-encode with altered keyframe interval)
    altered_keyframe_video_path = os.path.join(output_folder, "altered_keyframe.mp4")
    altered_frame_rate.write_videofile(
        altered_keyframe_video_path,
        codec="libx264",
        ffmpeg_params=["-g", "12"],  # Adjust keyframe interval
    )

    # 3. Pixel Shifting (Shift random pixels in non-consecutive frames)
    subtly_pixel_shifted_video = clip.fl(lambda gf, t: pixel_shift(gf(t), t))  # Pass actual frame to pixel_shift
    subtly_pixel_shifted_video_path = os.path.join(output_folder, "subtle_pixel_shifted.mp4")
    subtly_pixel_shifted_video.write_videofile(subtly_pixel_shifted_video_path)

    # 4. Audio Frequency Shifting (Slight change in audio frequency)
    altered_audio = original_audio.set_fps(original_audio.fps + 1)  # Slight frequency shift
    clip_with_altered_audio = clip.set_audio(altered_audio)
    altered_audio_video_path = os.path.join(output_folder, "altered_audio_frequency.mp4")
    clip_with_altered_audio.write_videofile(altered_audio_video_path)

    # 5. Add Subtle Noise to Video (Tiny luminance adjustment)
    subtly_noisy_video = clip.fx(vfx.lum_contrast, lum=0.01)  # Add tiny luminance noise
    subtly_noisy_video_path = os.path.join(output_folder, "subtle_noise.mp4")
    subtly_noisy_video.write_videofile(subtly_noisy_video_path)

    # 6. Slight Color Adjustment (Increase brightness by 5%)
    subtly_color_adjusted = clip.fx(vfx.colorx, 1.05)  # Slightly increase brightness
    subtly_color_adjusted_path = os.path.join(output_folder, "subtle_color_adjustment.mp4")
    subtly_color_adjusted.write_videofile(subtly_color_adjusted_path)

    # 7. Minor Aspect Ratio Change with Padding (Resize and pad to maintain aspect ratio)
    target_height = int(clip.h * 0.98)
    padded_clip = clip.resize(height=target_height).margin(
        top=(clip.h - target_height) // 2, bottom=(clip.h - target_height) // 2, color=(0, 0, 0)
    )
    padded_clip_path = os.path.join(output_folder, "subtle_aspect_ratio_change.mp4")
    padded_clip.write_videofile(padded_clip_path)

    # 8. Micro Rotation (Rotate by 1 degree)
    subtly_rotated = clip.rotate(1)  # Rotate by 1 degree
    subtly_rotated_path = os.path.join(output_folder, "subtle_rotation.mp4")
    subtly_rotated.write_videofile(subtly_rotated_path)

    # # 9. Slight Speed Change in Audio (Time Stretch - speed up by 1%)
    # subtly_sped_up_audio = speed_up_audio(original_audio, 1.01)  # Speed up by 1%
    # subtly_sped_up_clip = clip.set_audio(subtly_sped_up_audio)
    # subtly_sped_up_clip_path = os.path.join(output_folder, "subtle_audio_speedup.mp4")
    # subtly_sped_up_clip.write_videofile(subtly_sped_up_clip_path)

    # 10. Volume Adjustment (Increase volume slightly)
    altered_audio_volume = original_audio.volumex(1.05)  # Slight volume increase by 5%
    clip_with_altered_volume_audio = clip.set_audio(altered_audio_volume)
    altered_audio_volume_path = os.path.join(output_folder, "altered_audio_volume.mp4")
    clip_with_altered_volume_audio.write_videofile(altered_audio_volume_path)

    # 11. Combine All Alterations into Final Video
    final_clip = VideoFileClip(altered_keyframe_video_path)
    final_clip = final_clip.set_audio(clip_with_altered_volume_audio.audio)

    # Output Final Video
    final_output_path = os.path.join(output_folder, "final_altered_video.mp4")
    final_clip.write_videofile(final_output_path)

    print(f"Alterations completed. Final video saved at: {final_output_path}")

def main():
    input_video_path = r"C:\Users\Veenu_Gupta\Pictures\Camera Roll\WIN_20230806_19_59_20_Pro.mp4"  # Replace with your video file path
    output_folder = "altered_video_output"
    apply_alterations(input_video_path, output_folder)

if __name__ == "__main__":
    main()
