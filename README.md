CameraServer is used for providing a better web interface from my security camera for exploring the files stored on it. It also wraps a H.265 file in an MP4 container and can optionally save the converted MP4 file to the server or the user can download it to their device.

# Features/Task Checklist
 (Importance, lower more important/easier)
## Frontend
- [X] Create Frontend Web Page(s) (1)
- [ ] Implement error handling
  - [ ] HTTP Errors (4xx and 5xx)
- [ ] Implement downloading wrapped video for quick viewing, maybe make it secret.

## Backend/Server
- [/] Create Backend Endpoints (1)
- [X] Security
- Video & Image
  - [ ] Implement MP4 file wrapping for quick viewing (1)
  - [X] Implement MP4 file encoding (1) (encoding needed for browser play)
  - [X] Check if the file already exists on the server(1)
  - [X] Download file to server (2)
  - [ ] Implement storage limit warning (2)
  - [ ] Implement deleting old files when storage is full (2)
  - [ ] Handle video not finishing encoding 
- [X] Implement Camera DB files processing (2)
  - [ ] Implement auto updating database files if it is today's and thus not upto date.
- [ ] Implement path traversal protection (2)
- [ ] Implement error handling
  - [ ] HTTP Errors (4xx and 5xx)
- [/?] Handle a video not being finished recording yet on the camera. (1)
- [ ] Migrate to use SQLite (2)
- [ ] Implement redirecting to login screen if camera is attempted to be accessed without being logged in

## Deployment
- [X] Setup docker file
- [X] Create docker run file
- [X] Deploy a version

Will store files like this on the server:
```
CameraVideoServer/
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

# Local vs Camera databases
This server will have databases for all available media. Whether on the camera or on the server.
When data is deleted off the camera, local databases will be updated to reflect that, only storing
dates and filenames that are stored on the server.

# Security Vulnerability
Endpoint files don't need auth!
Including DB files, which means all paths are exposed in plaintext, making it easier to access/request them. No need for guessing!
Index page wouldn't work without auth because that required the HTML to be parsed, but any web pages require auth (while individual files, such as images, vids, and DBs dont)

I tested on a brand new firefox app with no cached data, and test with curl with no authorisation, e.g.:
`curl http://192.168.0.40/sd/20251021/images000/A25102106282600.jpg -o image.jpg`
`curl http://192.168.0.40/sd/20251021/images000/imgdata.db -o imagedata.db`

## Writeup
### How I found it
This security vulnerability was found whilst trying to secure this app.
I was trying to secure the downloading of data from the camera.
While doing this I noticed that the index date page required auth, but not the media date page or any of the media files.
This led me to thinking it was a problem in my app, maybe some cached or hardcoded auth values since it worked even on deployments via docker.
After confirming that it wasn't by seeing that `response.request.headers` contained:
```
2025-10-21 19:15:05,584 - global_logger - DEBUG - Request headers actually sent: {'User-Agent': 'python-requests/2.32.5', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': 'Basic None'}
```
Note the header of
```"Authorization": "Basic None"```
when it should have a Base64 value of the username and password in the format of `base64(<username>:<password>)` for proper authorisation.
For example, a username of admin and a password of password would make the header be `"Authorization": "YWRtaW46cGFzc3dvcmQ="`.
I still thought that maybe it was some cached data, but quickly gave up on that.
After some back and forth with ChatGPT I decided to test if the end points for the media files and database files even required auth.
And to my surprise, they didn't.
The reason I didn't realise this earlier was because I forgot that in my implementation of getting the media paths, I didn't parse the HTML like I did for the index page of dates, I instead downloaded the DB files, stored them, and used them.
After it was after realising that that none of the files on the camera required auth, which includes media and DB files.

### Risks
Anyone can access any file stored on the camera on the local network, or if they have access to the local network from the outside.
The fact that all individual files are vulnerable makes it much easier for an attacker to sort through all files and download them all without brute forcing the names.
The risk of this actually happening can depend on not only the network security, but any malicious or vulnerable apps on a device in the network.

### Mitigation
Barring any software/firmware updates, the best thing to do would be to put the camera on its own VLAN, and then have a trusted middleware app that runs on a trusted computer to act as an intermediary.
The intermediary app would have proper authentication for users.
Whether or not the app authenticated itself to the camera with the username and password the camera expects is irrelevant for the purpose of fetching stored media, but it is still important for viewing a live feed. 
This could make it harder to view the camera live feed depending on the developed apps functionality/capability.