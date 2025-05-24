from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript('KW3z81TqrHg')
for entry in transcript:
    print(f"{entry['start']} - {entry['start'] + entry['duration']}: {entry['text']}")








    