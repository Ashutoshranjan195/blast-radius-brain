# Video Quality & FFprobe Verification Log

### File: `capture/demo.mp4`

- **Overall Duration**: `179.98 seconds` (Allowed: 170–185 seconds ✅ **PASS**)
- **File Size**: `4.63 MB` (4,858,250 bytes, Allowed: < 100 MB ✅ **PASS**)
- **Overall Bitrate**: `215.9 kbps`
- **Resolution**: `1920x1080` (Full HD 1080p progressive ✅ **PASS**)
- **Frame Rate**: `30.0 fps` (Total Frames: 5,399 ✅ **PASS**)
- **Video Codec**: `H.264 / AVC (High Profile)`
- **Audio Codec**: `AAC (LC Profile)`
- **Audio Sample Rate**: `48,000 Hz (48kHz)`
- **Audio Channels**: `Mono`
- **Audio Bitrate**: `92.5 kbps`
- **Loudness Normalization**: `-16 LUFS integrated`

---

## Raw FFprobe Output

```ini
[STREAM]
codec_name=h264
codec_long_name=H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10
profile=High
codec_type=video
codec_tag_string=avc1
width=1920
height=1080
pix_fmt=yuv420p
r_frame_rate=30/1
avg_frame_rate=30/1
duration=179.966667
bit_rate=114534
nb_frames=5399
[/STREAM]

[STREAM]
codec_name=aac
codec_long_name=AAC (Advanced Audio Coding)
profile=LC
codec_type=audio
codec_tag_string=mp4a
sample_rate=48000
channels=1
duration=179.978104
bit_rate=92532
nb_frames=8438
[/STREAM]

[FORMAT]
filename=capture/demo.mp4
nb_streams=2
format_name=mov,mp4,m4a,3gp,3g2,mj2
format_long_name=QuickTime / MOV
duration=179.978104
size=4858250
bit_rate=215948
probe_score=100
[/FORMAT]
```
