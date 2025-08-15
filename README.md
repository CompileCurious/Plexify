# Plexify

Plexify is a Python utility that organizes and renames media files based on metadata from your Plex server. It is designed to help users maintain a consistent and informative file naming structure outside of Plex, using technical and descriptive metadata extracted from the media itself.

## Features

- Connects to your Plex server using your token and server URL
- Scans specified Plex libraries for movies and TV shows
- Extracts metadata such as title, year, resolution, codecs, and audio channels
- Renames files using customizable templates
- Optionally moves or copies files to new directories
- Supports dry-run mode for previewing changes
- Handles subtitles and extras intelligently
- Uses ffprobe to extract technical media details

## Requirements

- Python 3.7+
- Plex server with accessible API token
- ffprobe (part of ffmpeg) installed and available in PATH

## Installation

Clone the repository:
git clone https://github.com/CompileCurious/Plexify.git
cd Plexify

Install dependencies:
pip install -r requirements.txt

Ensure ffprobe is installed:
# On Debian/Ubuntu
sudo apt install ffmpeg

# On macOS with Homebrew
brew install ffmpeg

## Configuration

Create a config.yml file in the root directory. Example:

plex:
  token: YOUR_PLEX_TOKEN
  url: http://localhost:32400
  libraries:
    - Movies
    - TV Shows

output:
  path: /path/to/output
  move_files: false
  include_subtitles: true
  include_extras: false

naming:
  movie: "{title} ({year}) [{resolution}] [{video_codec}] [{audio_channels}ch]"
  episode: "{show} - S{season:02}E{episode:02} - {title} [{resolution}]"

## Usage

Run the script:
python plexify.py

To preview changes without modifying files:
python plexify.py --dry-run

## Notes

- The script uses the Plex API to gather metadata and ffprobe to extract technical details from media files.
- It does not modify your Plex library or database.
- Ensure your Plex server is accessible and your token is valid.

## License

MIT License. See LICENSE file for details.
