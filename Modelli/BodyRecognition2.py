import cv2
import time
import datetime
import os

def draw_camera_style_lines(frame):
    height, width = frame.shape[:2]
    color = (255, 255, 255)  # Colore bianco
    thickness = 2  # Spessore delle linee

    # Disegna le linee in alto a sinistra
    cv2.line(frame, (20, 20), (80, 20), color, thickness)
    cv2.line(frame, (20, 20), (20, 80), color, thickness)

    # Disegna le linee in alto a destra
    cv2.line(frame, (width - 80, 20), (width - 20, 20), color, thickness)
    cv2.line(frame, (width - 20, 20), (width - 20, 80), color, thickness)

    # Disegna le linee in basso a sinistra
    cv2.line(frame, (20, height - 20), (80, height - 20), color, thickness)
    cv2.line(frame, (20, height - 20), (20, height - 80), color, thickness)

    # Disegna le linee in basso a destra
    cv2.line(frame, (width - 80, height - 20), (width - 20, height - 20), color, thickness)
    cv2.line(frame, (width - 20, height - 20), (width - 20, height - 80), color, thickness)

def select_video_source():
    sources = [
        ("CAM 1", 0),
        ("CAM 2", 1)
    ]
    
    print("Seleziona la fonte video:")
    for i, (name, _) in enumerate(sources):
        print(f"{i}: {name}")
    
    choice = int(input("Inserisci il numero della fonte video: "))
    
    return sources[choice][0]

def main():
    output_folder = "videos"
    os.makedirs(output_folder, exist_ok=True)

    video_filename = os.path.join(output_folder, "output.mp4")
    
    # Apri entrambe le videocamere
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)
    
    if not cap1.isOpened() or not cap2.isOpened():
        print("Errore nell'apertura delle fonti video")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0
    frame_size1 = (int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #frame_size2 = (int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(video_filename, fourcc, fps, frame_size1)

    current_cap = cap1
    recording = False
    start_time = 0
    frame_count = 0

    # Schermo intero all'avvio
    cv2.namedWindow('Feed della videocamera', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Feed della videocamera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = current_cap.read()
        
        if not ret:
            print("Non riesco a catturare il frame")
            break

        if recording:
            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            record_time_str = f"Time: {int(elapsed_time)}s Frame: {frame_count}"
            cv2.putText(frame, record_time_str, (frame.shape[1] - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            out.write(frame)

        date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, date_time_str, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        draw_camera_style_lines(frame)
        
        cv2.imshow('Feed della videocamera', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            if recording:
                recording = False
                print("Registrazione fermata")
            else:
                recording = True
                start_time = time.time()
                frame_count = 0
                print("Registrazione avviata")
        #elif key == ord('c'):
           # if current_cap == cap1:
            #    current_cap = cap2
            #else:
            #    current_cap = cap1
            #print("Fonte video cambiata")

    cap1.release()
    #cap2.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
