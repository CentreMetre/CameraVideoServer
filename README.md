CameraServer is used for providing a better web interface from my security camera for exploring the files stored on it. It also wraps a H.265 file in an MP4 container and can optionally save the converted MP4 file to the server or the user can download it to their device.

# Features/Task Checklist
 (Importance, lower more important/easier)
## Frontend
- [/] Create Frontend Web Page(s) (1)
- [ ] Implement error handling
  - [ ] HTTP Errors (4xx and 5xx)

## Backend/Server
- [/] Create Backend Endpoints (1)
- [X] Implement MP4 file wrapping (1)
    - [ ] Check if the file already exists on the server(1)
    - [ ] Download file to server (2)
    - [ ] Implement storage limit warning (2)
    - [ ] Implement deleting old files when storage is full (2)
- [ ] Implement MP4 file encoding (1) (encoding needed for browser play)
- [X] Implement Camera DB files processing (2)
- [ ] Implement path traversal protection (2)
- [ ] Implement error handling
  - [ ] HTTP Errors (4xx and 5xx)

Unsure of if to ever wrap because it has problems in browsers. If ever sent to someone as needed and its played in browser it wont work.
Encoding is the best way to go.

Will store encoded files like:
```
CameraServer/
├─ files/
│  ├─ 20250901/
│  │  ├─ images000/
│  │  │  ├─ A25090106224300.jpg
│  │  ├─ record000/
│  │  │  ├─ A250901_062244_062258.mp4
│  │  │  ├─ P250901_000000_001000.mp4
│  │  ├─ imgdata.db
│  │  ├─ recdata.db
```