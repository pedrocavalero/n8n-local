from youtube_transcript_api import YouTubeTranscriptApi
import json
import sys

video_id = ""

# The n8n Execute Command node passes arguments after the script name.
# We expect the videoId as the first argument.
if len(sys.argv) > 1:
    video_id = sys.argv[1]
else:
    # If no video_id is passed, print an error to stderr and exit.
    # n8n will capture stderr in the 'errorDetails' output of the Execute Command node.
    print("Error: No video ID provided as a command line argument.", file=sys.stderr)
    sys.exit(1)

try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([item['text'] for item in transcript_list])
    # Print the transcript to stdout. n8n will capture this in the 'stdout' field.
    print(full_transcript)
except Exception as e:
    # If any error occurs during transcript fetching, print it to stderr and exit.
    print(f"Error fetching transcript for video ID '{video_id}': {e}", file=sys.stderr)
    sys.exit(1)
