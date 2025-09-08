# Better Lyrics - Saved Songs Directory

This directory contains all your saved songs and playlists from the Better Lyrics app.

## Files:
- `songs_library.json` - Contains all your saved songs with lyrics and metadata
- `playlists.json` - Contains your playlists and favorites
- `*.backup` - Backup files created when corruption is detected

## Data Structure:

### songs_library.json
Each song contains:
- `id` - Unique identifier
- `title` - Song title
- `artist` - Artist name
- `lyrics` - Formatted lyrics for display
- `original_lyrics` - Original pasted lyrics
- `created_at` - When the song was saved
- `last_played` - Last time the song was loaded
- `play_count` - How many times the song was played
- `is_favorite` - Whether the song is favorited

### playlists.json
Contains playlists as:
```json
{
  "Favorites": ["song-id-1", "song-id-2"],
  "My Playlist": ["song-id-3", "song-id-4"]
}
```

## Backup and Recovery:
- The app automatically creates backups if file corruption is detected
- You can manually backup these files to preserve your song library
- To reset everything, simply delete the JSON files (keep this README)
