# CHANGELOG

## [1.0.0] - 2025-06-15

### Added
- Support for CSV files with terms and definitions
- Support for ODS spreadsheets with multiple sheets
- Customizable grid layout with `--cols` and `--rows` options
- Command-line interface with comprehensive options
- Double-sided printing support with mirrored definitions
- Dynamic text sizing based on content length
- Title pages for each topic/section
- Sample files in the `samples` directory

### Changed
- Consolidated code into a single main script
- Moved helper scripts to `scripts/` directory
- Improved documentation with emoji headers and better examples

### Fixed
- Corrected ODS file generation and parsing
- Fixed command-line argument handling for single CSV files
- Resolved directory creation issues
- Fixed table generation and cell styling

## Planned Features

### [1.1.0] - Future Release
- Add option to change print orientation, i.e., print definition upside down so that flipping card shows the definition right-side up
- Support for custom fonts and colors
- Export to individual image files (PNG/JPG)
- Interactive web interface for previewing cards
- Support for including images in flashcards
