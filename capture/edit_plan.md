# Video Edit & Assembly Plan — Blast Radius Brain

This document records the exact FFmpeg commands and video pipeline used to assemble the 180-second judge demo video (`capture/demo.mp4`).

---

## 1. Frame Generation & Preprocessing
All frames are generated and verified at `1920x1080` from live Playwright captures (`capture/screenshots/`):
- `frame_01.png`: Problem banner overlay (`01_home.png`)
- `frame_02.png`: Blast radius hero with callout bounding boxes on path chips (`02_blast_radius.png`)
- `frame_03.png`: Zoomed Cypher query code box with lower-third overlay (`02_blast_radius.png`)
- `frame_04.png`: Ranked domain expert callout box for Maya Chen (`03_expert_finder.png`)
- `frame_05.png`: Decision provenance audit callout box (`04_decision.png`)
- `frame_06.png`: Honest unknown evidence layer callout box (`05_honest_unknown.png`)
- `frame_07a.png`: Full FalkorDB Browser at localhost:3000 (`06_graph_browser.png`)
- `frame_07b.png`: FalkorDB Browser running blast radius Cypher query (`07_graph_ledger_highlight.png`)
- `frame_08.png`: Split screen — left `08_seed_counts.png`, right `09_tests_passing.png`
- `frame_09.png`: Complete data model architecture and closing card (`10_architecture.png`)

---

## 2. Audio Synthesis & Normalization
Individual scene audio files are synthesized with Windows SpeechSynthesizer, delayed according to scene start times using `adelay`, mixed with `amix`, normalized to -16 LUFS with `loudnorm`, and padded to 180 seconds:
```bash
ffmpeg -y \
  -i capture/voice_part_0.wav -i capture/voice_part_1.wav -i capture/voice_part_2.wav \
  -i capture/voice_part_3.wav -i capture/voice_part_4.wav -i capture/voice_part_5.wav \
  -i capture/voice_part_6.wav -i capture/voice_part_7.wav -i capture/voice_part_8.wav \
  -filter_complex "[0:a]adelay=500|500[a0];[1:a]adelay=15500|15500[a1];[2:a]adelay=50500|50500[a2];[3:a]adelay=65500|65500[a3];[4:a]adelay=85500|85500[a4];[5:a]adelay=105500|105500[a5];[6:a]adelay=120500|120500[a6];[7:a]adelay=150500|150500[a7];[8:a]adelay=170500|170500[a8];[a0][a1][a2][a3][a4][a5][a6][a7][a8]amix=inputs=9:normalize=0,loudnorm,apad=whole_dur=180[out]" \
  -map "[out]" -ar 48000 -t 180 capture/voiceover.wav
```

---

## 3. Scene Video Encoding (1080p H.264 @ 30fps)
Each scene is encoded with H.264 video codec at 30 fps for its specified duration:
```bash
# Scene 1 (15s)
ffmpeg -y -loop 1 -i capture/scenes/frame_01.png -c:v libx264 -t 15 -pix_fmt yuv420p -r 30 capture/scenes/01_home.mp4

# Scene 2 (35s)
ffmpeg -y -loop 1 -i capture/scenes/frame_02.png -c:v libx264 -t 35 -pix_fmt yuv420p -r 30 capture/scenes/02_blast.mp4

# Scene 3 (15s)
ffmpeg -y -loop 1 -i capture/scenes/frame_03.png -c:v libx264 -t 15 -pix_fmt yuv420p -r 30 capture/scenes/03_cypher.mp4

# Scene 4 (20s)
ffmpeg -y -loop 1 -i capture/scenes/frame_04.png -c:v libx264 -t 20 -pix_fmt yuv420p -r 30 capture/scenes/04_expert.mp4

# Scene 5 (20s)
ffmpeg -y -loop 1 -i capture/scenes/frame_05.png -c:v libx264 -t 20 -pix_fmt yuv420p -r 30 capture/scenes/05_decision.mp4

# Scene 6 (15s)
ffmpeg -y -loop 1 -i capture/scenes/frame_06.png -c:v libx264 -t 15 -pix_fmt yuv420p -r 30 capture/scenes/06_unknown.mp4

# Scene 7a & 7b (15s + 15s = 30s)
ffmpeg -y -loop 1 -i capture/scenes/frame_07a.png -c:v libx264 -t 15 -pix_fmt yuv420p -r 30 capture/scenes/07a_browser.mp4
ffmpeg -y -loop 1 -i capture/scenes/frame_07b.png -c:v libx264 -t 15 -pix_fmt yuv420p -r 30 capture/scenes/07b_browser.mp4

# Scene 8 (20s)
ffmpeg -y -loop 1 -i capture/scenes/frame_08.png -c:v libx264 -t 20 -pix_fmt yuv420p -r 30 capture/scenes/08_tests.mp4

# Scene 9 (10s)
ffmpeg -y -loop 1 -i capture/scenes/frame_09.png -c:v libx264 -t 10 -pix_fmt yuv420p -r 30 capture/scenes/09_close.mp4
```

---

## 4. Scene Concatenation
Concatenate all 10 video clips seamlessly using FFmpeg concat demuxer:
```bash
ffmpeg -y -f concat -safe 0 -i capture/concat.txt -c copy capture/demo_silent.mp4
```

---

## 5. Audio-Video Multiplexing
Merge `capture/demo_silent.mp4` with `capture/voiceover.wav` using AAC 192kbps audio:
```bash
ffmpeg -y -i capture/demo_silent.mp4 -i capture/voiceover.wav -c:v copy -c:a aac -b:a 192k -shortest capture/demo.mp4
```

---

## 6. Thumbnail Extraction
Extract high-resolution thumbnail at 00:00:30 (where path chips are prominently visible):
```bash
ffmpeg -y -ss 00:00:30 -i capture/demo.mp4 -frames:v 1 capture/demo_thumbnail.png
```
