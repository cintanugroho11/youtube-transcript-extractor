#!/usr/bin/env python3
"""
Example usage of youtube_extractor.py
Contoh penggunaan youtube_extractor.py
"""

from youtube_extractor import get_transcript, get_video_info, summarize_text, fetch_free_proxy

# Example video: Heru Margianto - Cara Menulis Berita Hardnews
VIDEO_URL = "https://www.youtube.com/watch?v=MnSwOITLduY"

print("=" * 60)
print("YouTube Transcript Extractor - Example")
print("=" * 60)

# 1. Get video info
print("\n1. Video Info:")
info = get_video_info(VIDEO_URL)
if info:
    print(f"   Title: {info.get('title', 'N/A')}")
    print(f"   Author: {info.get('author', 'N/A')}")
    print(f"   Video ID: {info.get('video_id', 'N/A')}")

# 2. Fetch a free proxy (for cloud/VPS)
print("\n2. Fetching free proxy...")
proxy = fetch_free_proxy(country='ID')
if proxy:
    print(f"   Found proxy: {proxy}")
else:
    print("   No proxy found, using direct connection")

# 3. Get transcript
print("\n3. Extracting transcript...")
result = get_transcript(VIDEO_URL, languages=['id', 'en'], proxy=proxy)

if result['success']:
    print(f"   ✅ Success!")
    print(f"   Words: {result['word_count']}")
    print(f"   Language: {result['language']}")
    print(f"   Characters: {result['character_count']}")

    # 4. Summarize
    print("\n4. Summary:")
    summary = summarize_text(result['text'], max_sentences=3)
    print(f"   {summary}")

    # 5. Full text preview
    print("\n5. Full Text (first 500 chars):")
    print(f"   {result['text'][:500]}...")
else:
    print(f"   ❌ Error: {result['error']}")

print("\n" + "=" * 60)
