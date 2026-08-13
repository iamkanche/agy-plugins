# Scrum Domain Specification

## 1. Overview
Provides standardized Agile/Scrum backlog management and Product Backlog Item (PBI) creation for Antigravity developer workflows.

## 2. Included Skills & Commands
- `/kanche:scrum-pbi-create`: Generates structured Product Backlog Items with User Stories, Acceptance Criteria (Given/When/Then), Priority, Story Points, and Domain links under `.docs/product/{domain}/backlog/`.

## 3. Product Backlog Structure
- Domain backlog directory: `.docs/product/{domain}/backlog/`
- Backlog Index file: `.docs/product/{domain}/backlog.md` or `.docs/product/scrum/backlog.md`
- AI Model Assignment: `model: pro` (for requirements engineering & backlog item drafting).
