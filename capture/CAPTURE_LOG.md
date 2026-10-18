# Capture Artifacts Log — Blast Radius Brain

| File Path | Description |
|---|---|
| `capture/screenshots/01_home.png` | Streamlit app home screen with title "Blast Radius Brain — Aurora Labs", sidebar graph health, and example buttons. |
| `capture/screenshots/02_blast_radius.png` | Blast radius query result showing natural-language answer, interactive path chips, Cypher query, params, and raw rows. |
| `capture/screenshots/03_expert_finder.png` | Expert finder query result ranking Maya Chen #1 with 3 projects, roles, Cypher, and project arrays. |
| `capture/screenshots/04_decision.png` | Decision provenance query result attributing "Pause Helios rollout" to Nora Haddad with staging latency regression notes. |
| `capture/screenshots/05_honest_unknown.png` | Honest unknown test for "Who owns Project Phoenix?" showing deterministic warning rejecting hallucination. |
| `capture/screenshots/06_graph_browser.png` | FalkorDB Web Browser running at localhost:3000 showing company graph visualization and node clusters. |
| `capture/screenshots/07_graph_ledger_highlight.png` | FalkorDB Web Browser executing variable-length Cypher traversal highlighting the ledger-service blast radius subgraph. |
| `capture/screenshots/08_seed_counts.png` | High-resolution terminal capture of `python seed.py` executed twice, confirming exact 42 nodes & 85 relationships. |
| `capture/screenshots/09_tests_passing.png` | High-resolution terminal capture of `pytest -q` showing all 6 acceptance test suites passing in 1.01s. |
| `capture/screenshots/10_architecture.png` | High-resolution architecture diagram rendering all 5 node labels and 9 directed relationship types. |
| `capture/video_raw/` | Raw Playwright video captures recorded during automated browser traversal session. |
| `capture/scenes/` | Individual rendered scene video clips (`01_home.mp4` through `09_close.mp4`) with on-screen overlays. |
| `capture/terminal_logs/seed_counts.txt` | Raw terminal stdout text log from executing `seed.py` multiple times. |
| `capture/terminal_logs/pytest_passing.txt` | Raw terminal stdout text log from executing `pytest -q`. |
| `capture/voiceover.txt` | Clean voiceover script transcript (259 words, ≤ 450 words limit). |
| `capture/voiceover.wav` | Master normalized 180-second audio track (48kHz, -16 LUFS) with precise scene synchronization. |
| `capture/demo_silent.mp4` | Concatenated 1080p video stream (180.00 seconds, 30fps) without audio. |
| `capture/demo.mp4` | Final multiplexed 1080p H.264 MP4 video (179.98s, 4.63 MB, stereo AAC audio) ready for hackathon submission. |
| `capture/demo_thumbnail.png` | Extracted video thumbnail at 00:00:30 prominently displaying the traversed path chips. |
| `capture/demo_script.md` | Scene-by-scene script detailing timings, visual actions, on-screen text overlays, and voiceover text. |
| `capture/on_screen_text.json` | JSON structured log of all on-screen banners, callouts, and lower-third overlays with start/end timestamps. |
| `capture/edit_plan.md` | Technical document containing the exact FFmpeg encoding and assembly commands. |
| `capture/VIDEO_LOG.md` | Verification report containing ffprobe stream analysis, duration, audio codec, and file size. |
