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

def main():
    # Cartella di destinazione per il video
    output_folder = "/Scrivania/"
    os.makedirs(output_folder, exist_ok=True)

    # Nome del file video
    video_filename = os.path.join(output_folder, "output.mp4")
    
    # Apri la videocamera (0 indica la videocamera predefinita)
    cap = cv2.VideoCapture(0)
    
    # Verifica che la videocamera sia stata aperta correttamente
    if not cap.isOpened():
        print("Errore nell'apertura della videocamera")
        return

    # Impostazioni per la registrazione del video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)
    
    recording = False
    start_time = 0
    frame_count = 0

    while True:
        # Cattura frame per frame
        ret, frame = cap.read()
        
        if not ret:
            print("Non riesco a catturare il frame")
            break

        if recording:
            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Aggiungi tempo di registrazione e frame in alto a destra
            record_time_str = f"Time: {int(elapsed_time)}s Frame: {frame_count}"
            cv2.putText(frame, record_time_str, (frame.shape[1] - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Scrivi il frame nel file video
            out.write(frame)

        # Aggiungi data e ora in basso a sinistra
        date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, date_time_str, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Disegna le linee stile videocamera
        draw_camera_style_lines(frame)
        
        # Mostra il frame risultante
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
    
    # Rilascia il controllo della videocamera e chiudi le finestre
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
