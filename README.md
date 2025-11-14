sub-titles-auto-correct
=======================

[![Build Status](https://travis-ci.org/adrienbricchi/sub-titles-auto-correct.svg?branch=master)](https://travis-ci.org/adrienbricchi/sub-titles-auto-correct) [![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/adrienbricchi/sub-titles-auto-correct?svg=true&branch=master)](https://ci.appveyor.com/project/adrienbricchi/sub-titles-auto-correct?branch=master) [![Coverage Status](https://coveralls.io/repos/github/adrienbricchi/sub-titles-auto-correct/badge.svg?branch=master)](https://coveralls.io/github/adrienbricchi/sub-titles-auto-correct?branch=master)

Python script fixing OCR errors

## Installation

### Using pip (recommended)

```bash
pip install -e .
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

