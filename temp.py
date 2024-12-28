from moviepy.editor import VideoFileClip
from moviepy.audio.fx import audio_speedx

def speed_up_audio(audio, factor):
    # Apply the speed up effect to the audio
    return audio.fx(audio_speedx, factor)

def apply_alterations(input_video_path, output_folder):
    video = VideoFileClip(input_video_path)
    original_audio = video.audio

    # Speed up the audio by 1%
    subtly_sped_up_audio = speed_up_audio(original_audio, 1.01)

    # Combine the sped-up audio with the video
    video_with_audio = video.set_audio(subtly_sped_up_audio)

    # Output the altered video
    output_path = f"{output_folder}/subtly_sped_up_video.mp4"
    video_with_audio.write_videofile(output_path, codec="libx264")

def main():
    input_video_path = r"C:\Users\Veenu_Gupta\Pictures\Camera Roll\WIN_20230806_19_59_20_Pro.mp4"
    output_folder = "output_directory"
    apply_alterations(input_video_path, output_folder)

if __name__ == "__main__":
    main()
