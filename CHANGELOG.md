# Changelog - Better Lyrics

All notable changes to the Better Lyrics application will be documented in this file.

## [2.0.0] - 2025-09-07

### 🎵 NEW FEATURES

#### Complete Song Library System
- **Song History**: Automatic tracking of all transformed lyrics with timestamps
- **Favorites System**: Star songs for quick access in dedicated favorites tab
- **Recently Played**: Smart recent songs list with play counts and last accessed dates
- **Artist Organization**: Browse songs grouped by artist with song counts
- **Persistent Storage**: All songs saved locally in JSON format for privacy

#### Drag & Drop Integration  
- **Browser Support**: Drag selected text directly from Chrome, Firefox, Edge, or any browser
- **Universal Text Drag**: Works with any text selection from any application
- **Visual Feedback**: Drag zones highlight when text is being dragged over
- **Seamless Integration**: Automatically populates the lyrics input field

#### Smart Title/Artist Detection
- **Auto-Parsing**: Recognizes common formats like "Title - Artist", "Artist - Title", "Title by Artist"
- **Format Detection**: Handles brackets `[Artist] Title` and pipe separators `Title | Artist`
- **Smart Suggestions**: Pre-fills save dialog with detected title and artist
- **Manual Override**: Users can always edit auto-detected information

#### Enhanced Library UI
- **Tabbed Interface**: Organized tabs for All Songs, Recent, Favorites, and By Artist
- **Smart Sorting**: Different sorting for different views (alphabetical, recent, etc.)
- **Rich Song Items**: Display play counts, last played dates, and favorite status
- **Quick Actions**: Inline favorite toggle, play, and delete buttons

### 🔧 IMPROVEMENTS

#### User Experience
- **Larger Window**: Increased default size (1400x900) for better library viewing
- **Enhanced Pro Tips**: Updated guidance including drag & drop and formatting tips
- **Better Navigation**: Library button shows song count, clear visual states
- **Improved Messaging**: Contextual feedback for all user actions

#### Save System
- **Smart Save Dialog**: Auto-populated with detected title/artist information
- **Save Persistence**: Current song tracking prevents duplicate save prompts  
- **Library Integration**: Saved songs immediately appear in appropriate tabs
- **Play Statistics**: Automatic tracking of play counts and access times

#### Organization Features
- **Artist Grouping**: Dedicated view showing songs grouped by artist
- **Multiple Sort Options**: Sort by title, artist, or recent activity
- **Search-Ready Structure**: Foundation laid for future search functionality
- **Efficient Storage**: Optimized JSON structure for fast loading

### 🐛 BUG FIXES
- Fixed app exit issues with improved error handling
- Resolved UI rebuild problems with better state management
- Corrected drag handler event binding
- Fixed dialog positioning and responsive behavior

### 📚 TECHNICAL IMPROVEMENTS
- Added UUID-based song identification for reliable tracking
- Implemented robust JSON file handling with error recovery
- Enhanced regex patterns for title/artist parsing
- Improved container event handling for drag & drop
- Added proper datetime formatting for timestamps

## [1.0.1] - 2025-09-07

### Changed
- Updated default buffer lines from 12 to 4 for better user experience
- Users will now see lyrics appear immediately without confusion

## [1.0.0] - 2025-09-07

### Added
- Initial release of Better Lyrics desktop application
- Enhanced lyrics display with bold, centered formatting
- Dark mode and light mode themes with toggle button
- Smart lyrics formatting and cleanup
- Live customization controls:
  - Text alignment (left, center, right)
  - Font size slider (14-60pt)
  - Buffer lines slider (4-48 lines)
- Auto-scroll functionality with play/pause controls
- Dual scroll modes:
  - Manual speed control (0.1x to 5.0x speed)
  - Song length mode with time-based calculations (15s to 20min)
- Clipboard integration for easy paste and copy
- Professional UI with compact control layout
- Single executable distribution (no installation required)
- Version information and metadata for Windows
- Concept feature disclaimer for song length scroll calculations

---

**Note**: Version 2.0.0 represents a major upgrade from a simple lyrics formatter to a complete lyrics management system with library functionality, drag & drop support, and intelligent song organization.
