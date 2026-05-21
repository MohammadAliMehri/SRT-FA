# SrtFa — مترجم زیرنویس به فارسی

A Flask-based web application that translates `.srt` subtitle files from English to Persian (Farsi) using the Google Translate API — no API key required.

---

## Features

- **Drag-and-drop UI** — upload your `.srt` file directly from the browser
- **Batch translation** — groups subtitle blocks into batches for faster processing
- **Multi-threaded** — uses a thread pool to translate multiple batches in parallel
- **Persian text polishing** — automatically fixes half-spaces (`نیم‌فاصله`), plural suffixes, and replaces `?` / `,` with `؟` / `،`
- **Subtitle formatting** — wraps long lines to a readable width (42 chars, max 2 lines)
- **Live progress bar** — shows real-time translation progress in the browser
- **No API key needed** — uses Google Translate's free `gtx` endpoint

---

## Screenshot

> Upload an `.srt` file → click "شروع ترجمه" → download the translated file automatically.

---

## Project Structure

```
srt_fa/
├── app.py                     # Flask app & routes
├── requirements.txt
├── services/
│   ├── srt_parser.py          # Parses raw SRT lines into blocks
│   ├── srt_processor.py       # Batching & parallel translation logic
│   ├── translator.py          # Google Translate API wrapper
│   ├── persian_utils.py       # Persian text post-processing rules
│   └── subtitle_formatter.py  # Line-wrapping for subtitle display
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    └── index.html
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/MohammadAliMehri/SRT-FA.git
cd srt_fa
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open your browser at `http://127.0.0.1:5000`.

---

## Usage

1. Drag and drop (or click to select) an `.srt` subtitle file.
2. Click **شروع ترجمه** (Start Translation).
3. Wait for the progress bar to reach 100%.
4. The translated file (`translated.srt`) downloads automatically.

---

## Configuration

You can tweak these constants in `services/srt_processor.py`:

| Constant | Default | Description |
|---|---|---|
| `BATCH_SIZE` | `50` | Number of subtitle blocks per translation request |
| `MAX_THREADS` | `5` | Number of parallel worker threads |

---

## Dependencies

| Package | Version |
|---|---|
| Flask | 3.0.0 |
| requests | 2.31.0 |

---

## Disclaimer

This project uses Google Translate's unofficial free endpoint (`gtx`). It is intended for personal use only. For production or high-volume usage, use the official [Google Cloud Translation API](https://cloud.google.com/translate).

---

## License

MIT
