---
name: get-youtube-transcript
description: Fetch a transcript from a YouTube video URL and save as normalized JSON. Use when asked to get a youtube transcript, download youtube captions, or when given a YouTube URL to process.
---

# Get YouTube Transcript

## Overview

Fetch the transcript/captions from a YouTube video and save it as a normalized transcript JSON file ready for claim extraction.

## Input

YouTube URL as argument (required). Supports formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID&t=123`
- Just the video ID directly

## Process

### Step 1: Extract Video ID

Parse the YouTube URL to get the video ID. Handle all common URL formats.

### Step 2: Fetch Transcript

Run this via Bash:

```bash
uv run --with youtube-transcript-api python3 -c "
import json, sys, re

video_id = sys.argv[1]

# Extract video ID from URL if needed
patterns = [
    r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
    r'^([a-zA-Z0-9_-]{11})$'
]
for p in patterns:
    m = re.search(p, video_id)
    if m:
        video_id = m.group(1)
        break

from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript(video_id)
print(json.dumps(transcript))
" "URL_OR_VIDEO_ID"
```

This returns a JSON array: `[{"text": "...", "start": 0.5, "duration": 2.5}, ...]`

### Step 3: Get Video Metadata (Optional)

Try to get video title and channel name. If `yt-dlp` is available:

```bash
yt-dlp --dump-json --skip-download "URL" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({'title': d.get('title',''), 'channel': d.get('channel',''), 'upload_date': d.get('upload_date','')}))"
```

If `yt-dlp` is not available, ask the user for the podcast name and episode title, or derive from the URL.

### Step 4: Transform to Normalized Format

Convert the YouTube transcript data to the proof-please normalized format:

```json
{
  "doc_id": "yt__<channel_slug>__<title_slug>__<date>__v1",
  "source": {
    "type": "youtube_captions",
    "url": "<original_url>",
    "retrieved_at": "<today's date>"
  },
  "episode": {
    "podcast_name": "<channel name>",
    "title": "<video title>",
    "published_date": "<upload date or unknown>"
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
- `seg_id`: Sequential `seg_000001`, `seg_000002`, etc.
- `speaker`: Always `"Unknown"` (YouTube captions don't identify speakers)
- `start_time_s`: `round(start)` as integer seconds
- `text`: The `text` field from each caption entry
- Merge consecutive captions that are very short (< 3 words) into the previous segment to avoid fragments

### Step 5: Write Output

Write the normalized JSON to `data/transcripts/norm/<doc_id>.json`

### Step 6: Report

Print to the conversation:
- Video title and channel
- Number of segments extracted
- Total duration
- Output file path
- Suggest: "Run `/extract-claims <output_path>` to extract health claims from this transcript"

## Notes

- YouTube auto-generated captions are 60-85% accurate. They work well for health/science podcasts with clear speech.
- Some videos have no captions available. If the fetch fails, suggest using `/transcribe-audio` with a downloaded audio file instead.
- No API key or authentication required.
