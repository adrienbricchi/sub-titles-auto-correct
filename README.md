sub-titles-auto-correct
=======================

[![Build Status](https://travis-ci.org/adrienbricchi/sub-titles-auto-correct.svg?branch=master)](https://travis-ci.org/adrienbricchi/sub-titles-auto-correct) [![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/adrienbricchi/sub-titles-auto-correct?svg=true&branch=master)](https://ci.appveyor.com/project/adrienbricchi/sub-titles-auto-correct?branch=master) [![Coverage Status](https://coveralls.io/repos/github/adrienbricchi/sub-titles-auto-correct/badge.svg?branch=master)](https://coveralls.io/github/adrienbricchi/sub-titles-auto-correct?branch=master)

Python script fixing OCR errors

## Prerequisites

### Required

- **Python 3.6+**: The application requires Python 3.6 or higher
- **Python Tkinter**: Required for GUI mode
  - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
  - **Fedora/RHEL**: `sudo dnf install python3-tkinter`
  - **Arch Linux**: `sudo pacman -S tk`
  - **macOS**: Included with Python from python.org
  - **Windows**: Included with Python installer

### Optional

- **tkinterdnd2**: For drag-and-drop support in GUI mode
  - Install with: `pip install tkinterdnd2`
  - Without this, you can still use the "Add Files" button to select files
- **MS Word 2010+**: For MS Word spell check integration
- **LibreOffice Writer 6+**: For LibreOffice spell check integration

### Configuration

Before running the application, you need to configure the `config.ini` file:

```ini
[PARAMETERS]
root_path = /path/to/your/subtitles/directory
fix_sdh_tags = true
fix_3d_doubles = true
is_unittest_exec = false
auto_skip_everything = false

[DEPENDENCIES]
ms_word_2010_path = C:/Program Files/Microsoft Office/Office14/WINWORD.EXE
libreoffice6_writer_path = /usr/bin/libreoffice
```

**Configuration Options:**
- `root_path`: Directory containing .srt subtitle files (used in batch/script mode)
- `fix_sdh_tags`: Remove SDH (Deaf/Hard of Hearing) tags like [SOUND] and ♪
- `fix_3d_doubles`: Remove duplicate lines in 3D subtitles
- `is_unittest_exec`: Set to true when running unit tests
- `auto_skip_everything`: Skip all interactive prompts
- `ms_word_2010_path`: Path to MS Word executable
- `libreoffice6_writer_path`: Path to LibreOffice Writer executable

## Installation

### Using Virtual Environment (Recommended)

Modern Linux distributions use "externally-managed-environment" to protect system Python packages. It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows

# Install the package in editable mode
pip install -e .
```

**Note**: You'll need to activate the virtual environment each time you want to run the application:
```bash
source venv/bin/activate
python -m subtitles_auto_correct
```

**Quick Start**: For convenience, use the provided launcher script:
```bash
./run.sh
```
This script automatically activates the virtual environment and runs the application.

### Alternative: Using pip with --user flag

If you prefer not to use a virtual environment:

```bash
pip install --user -e .
```

### Alternative: System-wide installation (Not recommended)

On some systems, you can override the protection (use with caution):

```bash
pip install -e . --break-system-packages
```

### Running the application

```bash
# After installation
python -m subtitles_auto_correct

# Or directly
subtitles-auto-correct
```

When prompted, you can choose from:
- `script` - Automated batch corrections on all .srt files in configured directory
- `word` - MS Word spell check integration
- `libreoffice` - LibreOffice Writer spell check integration
- `gui` - **NEW!** Graphical interface with buttons for each correction type

### GUI Mode (New!)

The GUI provides a minimal tkinter interface with individual buttons for each correction type:

**Requirements:**
- Python 3 with tkinter (install with `sudo apt-get install python3-tk` on Ubuntu/Debian)

**Features:**
- **File Selection**: Browse and select any .srt subtitle file
- **Individual Corrections**: Apply specific corrections one at a time
- **Quick Corrections**: Apply all single-line, all multi-line, or all corrections at once
- **External Tools**: Launch MS Word or LibreOffice Writer for spell checking

**Available Correction Buttons:**

*Character Fixes:*
- Fix À (Accentuated A in French)
- Fix I → l (capital I to lowercase L)
- Fix V → v (capital V to lowercase)
- Fix 0 → o (zero to letter O)
- Fix l → I (lowercase L to capital I in acronyms)

*Punctuation Fixes:*
- Fix Punctuation Errors (ellipsis, dots, dashes)
- Fix Punctuation Spaces (?, !)
- Fix Dialog Hyphens (- spacing)
- Fix Degree Symbol (°)
- Fix Colons (:)
- Fix Quotes (" and ')

*Format Fixes:*
- Fix Italic Tags (<i></i>)
- Fix Common Errors (unicode quotes, dashes)
- Fix Numbers (spacing, formatting)
- Fix Acronyms (U.S. A → U.S.A)
- Fix Common Misspells (from CSV)

*Multi-Line Fixes:*
- Remove 3D Duplicates
- Remove Empty Lines
- Remove Redundant Italic Tags
- Remove/Add Dialog Hyphens
- Fix Double Quote Balance
- Remove SDH Tags ([SOUND], ♪, character labels)

*External Spell Checkers:*
- MS Word Spell Check
- LibreOffice Writer Spell Check

**Usage:**
```bash
python -m subtitles_auto_correct
# Choose "gui" when prompted
```

Or launch GUI directly:
```bash
python -m subtitles_auto_correct.gui
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/adrienbricchi/sub-titles-auto-correct.git
cd sub-titles-auto-correct

# Install in editable mode with development dependencies
pip install -e .

# Run tests
pytest
```

## License

License GPLv3+ : GNU GPL version 3 or later \<<http://gnu.org/licenses/gpl.html>\>.  
This is free software: you are free to change and redistribute it.  
There is NO WARRANTY, to the extent permitted by law.  

