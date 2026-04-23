# YouTube Transcript Extractor with Proxy Support

Extract transcripts from YouTube videos without API keys. Designed to work on cloud/VPS environments where YouTube blocks direct access.

---

## 🇬🇧 English

### Features
- **No API key required** — uses `youtube-transcript-api`
- **Proxy support** — bypass YouTube IP blocks on cloud servers (AWS, GCP, Azure, etc.)
- **Auto proxy fetch** — automatically fetches free proxies from ProxyScrape
- **Multi-language** — supports Indonesian (`id`) and English (`en`) transcripts
- **Video info** — get title, author, thumbnail via oEmbed (no key needed)
- **Summarization** — built-in extractive text summarization

### Installation

```bash
pip install youtube-transcript-api requests
```

### Quick Start

```python
from youtube_extractor import get_transcript

# Direct connection (works on local machines)
result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")

# With proxy (for cloud/VPS)
proxy = "socks4://103.166.32.130:11080"
result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID", proxy=proxy)

if result['success']:
    print(result['text'])
else:
    print(f"Error: {result['error']}")
```

### CLI Usage

```bash
# Direct connection
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# With proxy
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" "socks4://host:port"

# Auto-fetch proxy
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Proxy Sources

The `fetch_free_proxy()` function fetches from:
- [ProxyScrape Free Proxy List](https://www.proxyscrape.com/free-proxy-list)

Supported proxy formats:
- `socks4://host:port`
- `http://host:port`

### Why Proxy?

YouTube blocks transcript requests from cloud provider IPs (AWS, GCP, Azure, DigitalOcean, etc.). Using an Indonesian residential proxy bypasses this restriction.

---

## 🇮🇩 Bahasa Indonesia

### Fitur
- **Tidak perlu API key** — pakai `youtube-transcript-api`
- **Dukungan proxy** — lewati blokir IP YouTube di server cloud (AWS, GCP, Azure, dll)
- **Auto ambil proxy** — otomatis mengambil proxy gratis dari ProxyScrape
- **Multi-bahasa** — mendukung transkrip Bahasa Indonesia (`id`) dan Inggris (`en`)
- **Info video** — dapatkan judul, penulis, thumbnail via oEmbed (tanpa API key)
- **Ringkasan** — fitur ringkasan teks bawaan

### Instalasi

```bash
pip install youtube-transcript-api requests
```

### Penggunaan Cepat

```python
from youtube_extractor import get_transcript

# Koneksi langsung (berhasil di mesin lokal)
result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")

# Dengan proxy (untuk cloud/VPS)
proxy = "socks4://103.166.32.130:11080"
result = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID", proxy=proxy)

if result['success']:
    print(result['text'])
else:
    print(f"Error: {result['error']}")
```

### Penggunaan CLI

```bash
# Koneksi langsung
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Dengan proxy
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" "socks4://host:port"

# Auto-fetch proxy
python3 youtube_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Sumber Proxy

Fungsi `fetch_free_proxy()` mengambil dari:
- [ProxyScrape Free Proxy List](https://www.proxyscrape.com/free-proxy-list)

Format proxy yang didukung:
- `socks4://host:port`
- `http://host:port`

### Kenapa Perlu Proxy?

YouTube memblokir request transkrip dari IP cloud provider (AWS, GCP, Azure, DigitalOcean, dll). Menggunakan proxy residential Indonesia melewati pembatasan ini.

---

## License

MIT License — see [LICENSE](LICENSE)

## Author

**Cinta Nugroho** — cinta.nugroho11@gmail.com

---

*Built for the Openclaw pipeline. Extract, learn, improve.*
