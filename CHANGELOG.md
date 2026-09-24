# Changelog

All notable changes to **PDF Tool Lite** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.2] - 2026-09-24

### 🚀 Added
- **OS Native Drag & Drop:** Drop `.pdf` files directly from your desktop or file manager onto the application window to open them immediately.
- **Page Rotation Support:** Rotate selected PDF pages 90° Clockwise or Counter-Clockwise directly from the context menu or via keyboard shortcuts. Rotations are losslessly preserved upon saving.
- **Bidirectional Splitter Synchronization:**
  - Selecting pages on the visual grid with your mouse instantly populates the smart range input (e.g. `1-3, 5`).
  - Typing ranges in the input field dynamically updates page selections on the grid.
- **One-Click Metadata Wiper:** Added a dedicated "Wipe All Metadata" (🧹) button to instantly strip personal and tracking metadata for ultimate privacy.
- **Merger File Reordering Controls:** Added "Move Up" (▲) and "Move Down" (▼) buttons alongside native list reordering.
- **Visual Cursor Feedback:** Responsive wait cursor during processing and saving operations.

### 🐛 Fixed
- **Merger Filename Collision Bug:** Fixed an issue where multiple files with the same name from different directories could conflict when merging.
- **Missing File Extension Guard:** Enforced automatic `.pdf` extension validation across all save dialogs to prevent hidden files on Linux desktop environments.
- **Robust CI/CD Release Automation:** Configured `permissions: contents: write`, `workflow_dispatch`, and valid PNG icons for automated multi-platform binary & AppImage releases.

---

## [1.0.1] - 2026-09-24

### 🚀 Added
- AppImage packaging workflow for Linux x86_64 distributions.
- Dedicated vector-derived desktop icon (`assets/icon.png`).

### 🔧 Changed
- Upgraded release actions to include standalone binary and AppImage in GitHub Releases.

---

## [1.0.0] - 2026-09-24

### 🎉 Initial Release
- **Local-First Architecture:** 100% offline, zero telemetry, zero cloud dependency.
- **Core Modules:**
  - Page Splitter with smart range parsing (`1-5`, `odd`, `even`, `all`).
  - Multi-file PDF Merger.
  - Page Organizer with keyboard precision reordering (`Ctrl + Left/Right`) and deletion (`Delete`).
  - High-resolution DPI Image Exporter (PNG).
  - Metadata Editor (Title, Author, Subject, Creator).
- **Modern UI:** Responsive PyQt6 interface with Catppuccin-inspired Dark & Light themes and real-time English/Turkish (EN/TR) language switching.
