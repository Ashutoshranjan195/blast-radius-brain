"""
Synthesizes voiceover.wav for Blast Radius Brain using Windows SpeechSynthesizer
and normalizes it to 48kHz -16 LUFS with FFmpeg.
"""

import subprocess
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURE_DIR = os.path.join(BASE_DIR, "capture")
VOICE_TXT = os.path.join(CAPTURE_DIR, "voiceover.txt")
TEMP_WAV = os.path.join(CAPTURE_DIR, "voiceover_raw.wav")
FINAL_WAV = os.path.join(CAPTURE_DIR, "voiceover.wav")

# Scene voiceover segments with exact start timestamps (seconds) in the 180s video
SCENE_TIMINGS = [
    (0.5, "Vector RAG gives you similar documents. It cannot tell you what breaks when a service goes down. This is Blast Radius Brain, a company brain where the graph does the reasoning."),
    (15.5, "The agent traverses the dependency graph. Payments API breaks immediately. Checkout UI, two hops away, also breaks. Every affected system comes with the exact path the graph followed."),
    (50.5, "This is not a guess. This is the exact Cypher query. A variable-length traversal over DEPENDS_ON edges. Deterministic, auditable, fast enough to run on every agent step."),
    (65.5, "The same graph ranks experts by project overlap. Maya Chen has worked on three projects that use ledger-service. No embeddings. Just a join the graph already stores."),
    (85.5, "Every decision traces back to its author, the project it was made in, and the systems it affects. A decision with an audit trail built into the graph."),
    (105.5, "And when the graph doesn't know, it says so. No hallucination. The evidence layer is honest about missing data."),
    (120.5, "This is the graph underneath. Every answer you saw is a traversal over these nodes and edges. The FalkorDB Browser shows the same query running live, and the same subgraph the agent used."),
    (150.5, "The seed is idempotent: running it twice produces the same graph. The tools are deterministic. The tests pass. This is a working system, not a mockup."),
    (170.5, "Blast Radius Brain. A company brain where the graph is the reasoning layer, and every answer ships with its evidence.")
]


def generate_voiceover():
    # Build PowerShell script to synthesize speech at exact timestamps
    ps_lines = [
        'Add-Type -AssemblyName System.Speech',
        '$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer',
        '$synth.Rate = 0',
        '$synth.Volume = 100',
        # Choose natural female or male voice
        '$voices = $synth.GetInstalledVoices()',
        'foreach ($v in $voices) { if ($v.VoiceInfo.Name -like "*Zira*" -or $v.VoiceInfo.Name -like "*David*") { $synth.SelectVoice($v.VoiceInfo.Name); break } }',
    ]

    # Synthesize individual WAV files for each scene
    temp_files = []
    for i, (start_sec, text) in enumerate(SCENE_TIMINGS):
        part_wav = os.path.join(CAPTURE_DIR, f"voice_part_{i}.wav").replace("\\", "/")
        temp_files.append((start_sec, part_wav))
        safe_text = text.replace("'", "''")
        ps_lines.append(f"$synth.SetOutputToWaveFile('{part_wav}')")
        ps_lines.append(f"$synth.Speak('{safe_text}')")

    ps_lines.append('$synth.Dispose()')
    ps_script = "; ".join(ps_lines)

    print("Synthesizing audio segments with Windows Speech...")
    subprocess.run(["powershell", "-Command", ps_script], check=True)

    # Use FFmpeg to mix segments into a single 180-second track with proper timing
    # ffmpeg adelay filter delays each audio stream by start_sec * 1000 ms
    inputs = []
    delays = []
    for i, (start_sec, part_wav) in enumerate(temp_files):
        inputs.extend(["-i", part_wav])
        delay_ms = int(start_sec * 1000)
        delays.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")

    mix_inputs = "".join([f"[a{i}]" for i in range(len(temp_files))])
    filter_complex = f"{';'.join(delays)};{mix_inputs}amix=inputs={len(temp_files)}:normalize=0,loudnorm,apad=whole_dur=180[out]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "48000",
        "-t", "180",
        FINAL_WAV
    ]

    print("Assembling and normalizing master voiceover (180s, 48kHz, -16 LUFS)...")
    subprocess.run(cmd, check=True)

    # Clean up temporary parts
    for _, part_wav in temp_files:
        if os.path.exists(part_wav):
            try:
                os.remove(part_wav)
            except Exception:
                pass

    print(f"Master voiceover saved to: {FINAL_WAV}")


if __name__ == "__main__":
    generate_voiceover()
