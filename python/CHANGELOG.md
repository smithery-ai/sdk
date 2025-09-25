# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-09-25

### Added
- New `start` command specifically for production deployment

### Fixed
- Fixed bug where optional configuration parameters were incorrectly rejected as invalid

## [0.2.4] - 2025-09-19

### Changed
- Removed verbose logging from fastmcp_patch for cleaner output

## [0.2.3] - 2025-09-19

### Fixed
- Fixed well-known endpoint by using Starlette for response handling

## [0.2.1] - 2025-09-19

### Fixed
- Updated scope and host header handling in fastmcp_patch for better compatibility with proxy

## [0.2.0] - 2025-09-19

### Added
- Well-known MCP configuration endpoint (`/.well-known/mcp-config`) to expose session configuration schema
