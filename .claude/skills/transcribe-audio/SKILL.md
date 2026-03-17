---
name: transcribe-audio
description: Transcribe a local audio or video file using OpenAI Whisper. Use when asked to transcribe audio, transcribe a podcast, use whisper, transcribe video, or do local transcription.
---

# Transcribe Audio with Whisper

## Overview

Transcribe a local audio or video file using OpenAI's Whisper large-v3 model running locally. Produces a normalized transcript JSON file ready for claim extraction.

## Input

Path to an audio or video file as argument (required). Supported formats: `.mp3`, `.mp4`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.webm`, `.avi`, `.mkv`

## Prerequisites

- **ffmpeg** must be installed system-wide (`brew install ffmpeg` on macOS)
- **First run note**: The Whisper large-v3 model (~3GB) will be downloaded automatically on first use. This takes a few minutes.

## Process

### Step 1: Validate Input

Check that the input file exists and has a supported extension.

### Step 2: Extract Audio

Convert the input to 16kHz mono WAV using ffmpeg:

```bash
ffmpeg -i "<input_file>" -acodec pcm_s16le -ac 1 -ar 16000 "/tmp/pp_whisper_audio.wav" -y -loglevel error
```

### Step 3: Transcribe with Whisper

Run Whisper via inline Python with ad-hoc dependency:

```bash
uv run --with openai-whisper python3 -c "
import whisper, json, sys, gc

audio_path = sys.argv[1]
output_path = sys.argv[2]

print('Loading Whisper large-v3 model...', file=sys.stderr)
model = whisper.load_model('large-v3')

print('Transcribing...', file=sys.stderr)
result = model.transcribe(audio_path, word_timestamps=True, verbose=False)

del model
gc.collect()

output = {
    'text': result['text'].strip(),
    'language': result['language'],
    'segments': []
}

for seg in result['segments']:
    segment_data = {
        'id': seg['id'],
        'start': seg['start'],
        'end': seg['end'],
        'text': seg['text'].strip(),
    }
    if 'words' in seg:
        segment_data['words'] = [
            {'word': w['word'], 'start': w['start'], 'end': w['end'], 'probability': w.get('probability', 0.0)}
            for w in seg['words']
        ]
    output['segments'].append(segment_data)

with open(output_path, 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'Transcription complete: {len(output[\"segments\"])} segments, language: {output[\"language\"]}', file=sys.stderr)
" "/tmp/pp_whisper_audio.wav" "WHISPER_OUTPUT_PATH"
```

Save the raw Whisper JSON to `data/transcripts/whisper/<basename>.json`

### Step 4: Transform to Normalized Format

Convert the Whisper output to the proof-please normalized format:

```json
{
  "doc_id": "whisper__<basename>__v1",
  "source": {
    "type": "local_whisper",
    "file": "<original_file_path>",
    "retrieved_at": "<today's date>"
  },
  "episode": {
    "podcast_name": "Unknown",
    "title": "<filename without extension>",
    "published_date": "unknown"
  },
  "segments": [
    {
      "seg_id": "seg_000001",
      "speaker": "Unknown",
      "start_time_s": 0,
      "text": "..."
    }
  ]
}
```

Transformation rules:
- `seg_id`: Sequential `seg_000001`, `seg_000002`, etc. (map from Whisper's `id` field)
- `speaker`: Always `"Unknown"` (Whisper doesn't do speaker diarization)
- `start_time_s`: `round(start)` as integer seconds
- `text`: The `text` field from each Whisper segment
- Ask the user for podcast name, episode title, and date if they want accurate metadata. Otherwise use filename-derived defaults.

### Step 5: Write Output

Write the normalized JSON to `data/transcripts/norm/<doc_id>.json`

### Step 6: Clean Up

Remove the temporary WAV file at `/tmp/pp_whisper_audio.wav`

### Step 7: Report

Print to the conversation:
- Detected language
- Number of segments
- Total duration (last segment end time)
- Raw Whisper output path
- Normalized output path
- Suggest: "Run `/extract-claims <output_path>` to extract health claims from this transcript"

## Notes

- Whisper large-v3 is the most accurate model but requires ~10GB RAM. If memory is an issue, the skill can fall back to `medium` or `small` models.
- Transcription speed on Apple Silicon (M1/M2/M3): roughly 1 minute of processing per 5-10 minutes of audio for large-v3.
- For faster transcription on Apple Silicon, consider `mlx-whisper` as a future alternative.
