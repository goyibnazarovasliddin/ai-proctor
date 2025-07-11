from deepface import DeepFace
import os

KNOWN_FACES_DIR = "face_images"

def recognize_face_from_path(frame_path):
    min_distance = float("inf")
    identified_name = None

    for filename in os.listdir(KNOWN_FACES_DIR):
        user_image_path = os.path.join(KNOWN_FACES_DIR, filename)
        try:
            result = DeepFace.verify(
                img1_path=frame_path,
                img2_path=user_image_path,
                model_name="Facenet",
                enforce_detection=False
            )
            distance = result.get("distance", 1.0)
            if result["verified"] and distance < min_distance:
                min_distance = distance
                identified_name = os.path.splitext(filename)[0].replace("_", " ")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    return identified_name