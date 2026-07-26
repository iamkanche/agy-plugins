# Dev Workflows Specification

## 1. Overview
Provides incremental implementation and test execution capabilities for targeted code modifications.

## 2. Included Skills & Commands
- `/kanche:code-implement`: Implements target code changes incrementally, runs tests, and verifies correctness.

## 3. Product Invariants
- Operates under `@coder` subagent instructions.
- Verification required before declaring completion.
