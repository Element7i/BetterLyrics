#!/usr/bin/env python3
"""
Test script to verify the saved songs container is working properly.
"""

import json
import os
import sys

def test_saved_songs_container():
    """Test if the saved songs container is set up correctly."""
    
    # Check if saved_songs directory exists
    saved_songs_dir = "saved_songs"
    if not os.path.exists(saved_songs_dir):
        print("❌ saved_songs directory does not exist!")
        return False
    
    print(f"✅ saved_songs directory exists at: {os.path.abspath(saved_songs_dir)}")
    
    # Check directory contents
    contents = os.listdir(saved_songs_dir)
    print(f"📁 Directory contents: {contents}")
    
    # Check if README exists
    readme_path = os.path.join(saved_songs_dir, "README.md")
    if os.path.exists(readme_path):
        print("✅ README.md exists")
    else:
        print("❌ README.md missing")
    
    # Check if we can create test files
    try:
        test_songs_file = os.path.join(saved_songs_dir, "songs_library.json")
        test_playlists_file = os.path.join(saved_songs_dir, "playlists.json")
        
        # Test creating songs library
        test_song = {
            "id": "test-123",
            "title": "Test Song",
            "artist": "Test Artist",
            "lyrics": "Test lyrics content",
            "original_lyrics": "Test lyrics content",
            "created_at": "2025-09-07T12:00:00",
            "last_played": None,
            "play_count": 0,
            "is_favorite": False
        }
        
        with open(test_songs_file, 'w', encoding='utf-8') as f:
            json.dump([test_song], f, indent=2, ensure_ascii=False)
        
        print("✅ Successfully created test songs_library.json")
        
        # Test creating playlists
        test_playlists = {
            "Favorites": ["test-123"]
        }
        
        with open(test_playlists_file, 'w', encoding='utf-8') as f:
            json.dump(test_playlists, f, indent=2, ensure_ascii=False)
        
        print("✅ Successfully created test playlists.json")
        
        # Test reading files back
        with open(test_songs_file, 'r', encoding='utf-8') as f:
            loaded_songs = json.load(f)
        
        with open(test_playlists_file, 'r', encoding='utf-8') as f:
            loaded_playlists = json.load(f)
        
        print(f"✅ Successfully loaded {len(loaded_songs)} songs and {len(loaded_playlists)} playlists")
        
        # Clean up test files
        os.remove(test_songs_file)
        os.remove(test_playlists_file)
        print("✅ Test files cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing file operations: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Better Lyrics Saved Songs Container")
    print("=" * 50)
    
    success = test_saved_songs_container()
    
    if success:
        print("\n✅ All tests passed! The saved songs container is working correctly.")
        print("\n📋 Next steps:")
        print("1. Run the Better Lyrics app")
        print("2. Add some lyrics and save a song")
        print("3. Check the saved_songs/ directory for your files")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the setup.")
        sys.exit(1)
