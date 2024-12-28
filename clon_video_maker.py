import cv2
import numpy as np
import face_recognition
from moviepy.editor import VideoFileClip


def load_face_encoding(source_face_path):
    """
    Load the face encoding of the source image.
    """
    source_image = face_recognition.load_image_file(source_face_path)
    face_locations = face_recognition.face_locations(source_image)
    if len(face_locations) == 0:
        raise ValueError("No face found in the source image.")

    return face_recognition.face_encodings(source_image, face_locations)[0]


def swap_faces(frame, target_face_encoding, source_face_image, source_face_encoding):
    """
    Perform face swapping on a single video frame.
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        match = face_recognition.compare_faces([target_face_encoding], face_encoding)
        if match[0]:
            # Replace face with source face
            face_width = right - left
            face_height = bottom - top
            source_face_resized = cv2.resize(source_face_image, (face_width, face_height))
            frame[top:bottom, left:right] = source_face_resized

    return frame


def clone_video(video_path, output_path, source_face_path):
    """
    Clone a video by replacing target faces with a source face.
    """
    print("Loading source face...")
    source_face_encoding = load_face_encoding(source_face_path)
    source_face_image = face_recognition.load_image_file(source_face_path)

    print("Processing video...")
    clip = VideoFileClip(video_path)
    target_face_encoding = source_face_encoding  # In this example, assume single face.

    def process_frame(frame):
        return swap_faces(frame, target_face_encoding, source_face_image, source_face_encoding)

    processed_clip = clip.fl_image(process_frame)
    processed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("Video cloning completed. Output saved to", output_path)


if __name__ == "__main__":
    video_path = r"C:\Users\Veenu_Gupta\Pictures\Camera Roll\WIN_20240727_11_33_39_Pro.mp4"  # Input video file
    output_path = "output_video.mp4"  # Output video file
    source_face_path = r"C:\Users\Veenu_Gupta\Pictures\LG.jpg"  # Source face image

    clone_video(video_path, output_path, source_face_path)
