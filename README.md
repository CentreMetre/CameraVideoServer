CameraServer is used for providing a better web interface from my security camera for exploring the files stored on it. It also wraps a H.265 file in an MP4 container and can optionally save the converted MP4 file to the server or the user can download it to their device.

# Features/Task Checklist
 (Importance, lower more important/easier)
## Frontend
- [/] Create Frontend Web Page(s) (1) 
## Backend/Server
- [/] Create Backend Endpoints (1)
- [ ] Implement MP4 file wrapping (1)
    - [ ] Check if the file already exists on the server(1)
    - [ ] Download file to server (2)
    - [ ] Implement storage limit warning (2)
    - [ ] Implement deleting old files when storage is full (2)
- [X] Implement Camera DB files processing (2)