# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-11-03

### Added
- Complete project restructure with modular architecture
- Proper logging system with configurable log levels
- Configuration file support (YAML/JSON)
- Multiple output formats (CSV, JSON, TXT)
- Resume capability with checkpoint files
- Progress bars for visual feedback
- Multiple browser engine support (Chrome, Firefox, Edge)
- Rate limiting to prevent IP bans
- URL validation and error handling
- Type hints throughout codebase
- Comprehensive unit tests
- CI/CD pipeline configuration
- Concurrent scraping support for multiple URLs
- Export options with customizable fields
- Better error messages and user feedback

### Changed
- Split monolithic script into modular components
- Updated user-agent to modern version
- Improved anti-bot detection measures
- Made timeouts configurable
- Enhanced documentation with examples

### Fixed
- Corrected installation instructions (removed argparse)
- Added proper error handling for network failures
- Fixed memory efficiency issues
- Improved duplicate detection

## [1.0.0] - Initial Release

### Added
- Basic Substack archive scraping
- Infinite scroll handling
- Debug mode
- Date sorting and display
- Command-line interface
