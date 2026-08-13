# Scrum Domain Specification

## 1. Overview
Provides standardized Agile/Scrum backlog management and Product Backlog Item (PBI) creation for Antigravity developer workflows.

## 2. Included Skills & Commands
- `/kanche:scrum-pbi-create`: Generates structured Product Backlog Items with User Stories, Acceptance Criteria (Given/When/Then), Priority, Story Points, and Domain links under `.docs/backlog/{domain}/`.

## 3. Product Backlog Structure
- Backlog directory: `.docs/backlog/{domain}/`
- Backlog Index file: `.docs/backlog/{domain}/backlog.md`
- AI Model Assignment: `model: pro` (for requirements engineering & backlog item drafting).
