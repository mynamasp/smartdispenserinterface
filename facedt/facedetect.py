import face_recognition
import cv2
import os
import glob

# Global Variables
users_dir = 'C:/Users/prasa/smartdispenser/facedt/users'  # Path where user directories are stored
output_dir = 'C:/Users/prasa/smartdispenser/flaskProject'  # Path where you want to store the output files


def load_user_data(user_folder):
    try:
        face_encodings = []
        for image_filename in glob.glob(os.path.join(user_folder, 'face*.jpg')):
            image = face_recognition.load_image_file(image_filename)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_encodings.append(encodings[0])

        if not face_encodings:
            raise ValueError(f"No face encodings found in {user_folder}")

        # Read userID and userPIN
        with open(os.path.join(user_folder, 'userID.txt'), 'r') as f:
            user_id = f.read().strip()
        with open(os.path.join(user_folder, 'userPIN.txt'), 'r') as f:
            user_pin = f.read().strip()

        return face_encodings, user_id, user_pin
    except Exception as e:
        print(f"Error loading data for {user_folder}: {e}")
        return None, None, None


def recognize_face(face_encodings, frame):
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        for reference_encoding in face_encodings:
            matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.6)
            if True in matches:
                return True
    return False


def capture_face_from_webcam():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()
    return frame if ret else None

def write_output_file(is_recognized, user_id):
    output_file_path = os.path.join(output_dir, 'user.txt')
    mode = 'a' if is_recognized else 'w'  # Append if recognized, overwrite otherwise
    with open(output_file_path, mode) as file:
        if is_recognized:
            # Clear existing content if a user is recognized
            file.truncate(0)
            file.write(user_id + '\n')  # Append user ID with newline character
        else:
            # Truncate the file if no user is recognized
            file.truncate(0)
def main():
    frame = capture_face_from_webcam()
    if frame is None:
        print("Error: Webcam not accessible or no image captured.")
        return

    # Filter out system directories
    user_folders = [f for f in os.listdir(users_dir) if
                    os.path.isdir(os.path.join(users_dir, f)) and not f.startswith('.')]

    # Iterate over each user directory and attempt face recognition
    for user_folder_name in user_folders:
        user_folder_path = os.path.join(users_dir, user_folder_name)
        face_encodings, user_id, user_pin = load_user_data(user_folder_path)
        if face_encodings:
            recognized = recognize_face(face_encodings, frame)
            if recognized:
                print(f"User recognized: {user_id}")
                write_output_file(True, user_id)
                return  # Exit the function once a user is recognized
    # No user was recognized after checking all folders
    print("No user recognized.")
    write_output_file(False, None)


if __name__ == '__main__':
    main()
