#!/usr/bin/env python3
"""
youtube_extractor.py
Extract transcript from YouTube videos using youtube-transcript-api.
No API key needed. Works with any public video that has captions.
Supports proxy for bypassing IP blocks on cloud/VPS environments.

Author: Cinta Nugroho
License: MIT
"""

import re
import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    raise ImportError(
        "youtube-transcript-api not installed. Run: pip install youtube-transcript-api"
    )


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]

    parsed = urlparse(url)
    if parsed.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query).get('v', [None])[0]
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        elif parsed.path.startswith('/shorts/'):
            return parsed.path.split('/')[2]

    # Regex fallback
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(
    url: str,
    languages: list = ['id', 'en'],
    proxy: Optional[str] = None
) -> Dict:
    """
    Extract transcript from YouTube video.

    Args:
        url: YouTube video URL
        languages: Preferred languages (default: Indonesian, English)
        proxy: Proxy URL for bypassing IP blocks
               Examples:
               - 'socks4://103.166.32.130:11080'
               - 'http://103.65.237.92:5678'

    Returns:
        dict with success, text, language, word_count
    """
    video_id = extract_video_id(url)
    if not video_id:
        return {'success': False, 'error': 'Invalid YouTube URL', 'text': None}

    # Configure proxy if provided
    if proxy:
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=languages)

        full_text = ' '.join([snippet.text for snippet in transcript])

        # Detect language
        detected_lang = 'id' if any(
            w in full_text.lower()
            for w in ['yang', 'dan', 'dari', 'ini', 'dengan', 'untuk']
        ) else 'en'

        return {
            'success': True,
            'text': full_text,
            'language': detected_lang,
            'video_id': video_id,
            'word_count': len(full_text.split()),
            'character_count': len(full_text)
        }

    except TranscriptsDisabled:
        return {
            'success': False,
            'error': 'Transcripts disabled by video owner',
            'text': None,
            'video_id': video_id
        }
    except NoTranscriptFound:
        return {
            'success': False,
            'error': 'No transcript available for this video',
            'text': None,
            'video_id': video_id
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'text': None,
            'video_id': video_id
        }


def get_video_info(url: str) -> Optional[Dict]:
    """Get video title and author via oEmbed API (no key needed)."""
    video_id = extract_video_id(url)
    if not video_id:
        return None

    try:
        import requests
        oembed_url = (
            f"https://www.youtube.com/oembed?"
            f"url=https://www.youtube.com/watch?v={video_id}&format=json"
        )
        response = requests.get(oembed_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'video_id': video_id,
                'title': data.get('title'),
                'author': data.get('author_name'),
                'thumbnail': data.get('thumbnail_url')
            }
    except Exception:
        pass

    return {'video_id': video_id}


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """Extractive summary - first N sentences."""
    sentences = text.split('. ')
    summary = '. '.join(sentences[:max_sentences])
    if not summary.endswith('.'):
        summary += '.'
    return summary


def fetch_free_proxy(country: str = 'ID') -> Optional[str]:
    """
    Fetch a free proxy from ProxyScrape API.

    Args:
        country: Country code (default: ID for Indonesia)

    Returns:
        Proxy URL string or None
    """
    try:
        import requests
        url = (
            f"https://api.proxyscrape.com/v3/free-proxy-list/get?"
            f"request=displayproxies&proxy_format=protocolipport&"
            f"format=text&country={country}"
        )
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            proxies = response.text.strip().split('\n')
            for proxy in proxies:
                if proxy.strip():
                    return proxy.strip()
    except Exception:
        pass
    return None


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 youtube_extractor.py <YOUTUBE_URL> [proxy]")
        print("Example: python3 youtube_extractor.py 'https://youtu.be/VIDEO_ID' socks4://host:port")
        sys.exit(1)

    url = sys.argv[1]
    proxy = sys.argv[2] if len(sys.argv) > 2 else None

    # If no proxy provided, try to fetch one
    if not proxy:
        print("Fetching free proxy...")
        proxy = fetch_free_proxy()
        if proxy:
            print(f"Using proxy: {proxy}")
        else:
            print("No proxy available, trying direct connection...")

    result = get_transcript(url, proxy=proxy)

    if result['success']:
        print(f"✅ Transcript extracted ({result['word_count']} words)")
        print(f"Language: {result['language']}")
        print(f"\n📋 Summary (first {min(5, result['word_count'])} sentences):")
        print(summarize_text(result['text']))
        print(f"\n📝 Full text ({result['character_count']} chars):")
        print(
            result['text'][:2000] + "..."
            if len(result['text']) > 2000
            else result['text']
        )
    else:
        print(f"❌ Error: {result['error']}")
