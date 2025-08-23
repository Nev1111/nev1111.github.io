# Mystery Template System Documentation

## Overview

The Masha & Panda Mystery Template System provides a standardized Jekyll-based workflow for creating educational accounting mysteries that teach Python/pandas skills through engaging storytelling.

## Template Structure

### 1. Jekyll Layout
- **File**: `_layouts/mystery.html`
- **Purpose**: Provides consistent HTML structure for all mystery posts
- **Features**: Metadata display, navigation, character focus, skills covered

### 2. Content Template
- **File**: `_includes/mystery-template.md`
- **Purpose**: Markdown template for creating new mystery posts
- **Usage**: Copy template, replace placeholders, create engaging content

## Frontmatter Schema

### Required Fields
```yaml
layout: mystery
title: "Mystery Title"
mystery_number: 1
series: "Masha & Panda Mysteries"
difficulty_level: "beginner|intermediate|advanced"
estimated_time: "X minutes"
date: YYYY-MM-DD
```

### Content Organization Fields
```yaml
skills_covered: [skill1, skill2, skill3]
categories: [mysteries, topic_area]
tags: [pandas, python, specific_tags]
```

### Character & Story Fields
```yaml
real_scenario: true
character_focus: "masha|panda|both"
previous_mystery: "url"
next_mystery: "url"
```

## Content Structure

### 1. The Case
- **Opening**: Set scene, introduce the problem
- **Investigation**: Walk through what happened
- **Character Commentary**: Masha & Panda insights in blockquotes
- **Resolution**: How the problem was solved

### 2. The Solution
- **Code Block**: Python/pandas implementation
- **Comments**: Explain the technical approach

### 3. Key Learning Points
- **Bullet List**: 3-5 main takeaways
- **Educational Value**: Connect to broader concepts

## Character Guidelines

### Masha (The Analyst)
- Represents the accountant's inner voice wanting efficiency
- Often frustrated with tedious manual work
- Quick to spot patterns and inconsistencies
- Focuses on practical solutions

### Panda (The Wise Guide)
- Represents expertise without intimidation
- Offers different perspectives and approaches
- Encourages looking at problems from new angles
- Provides technical insights gently

## Usage Workflow

1. **Copy Template**: Use `_includes/mystery-template.md` as starting point
2. **Replace Placeholders**: Fill in all `{{placeholder}}` values
3. **Write Story**: Create engaging narrative around real accounting scenario
4. **Add Characters**: Include Masha & Panda commentary in blockquotes
5. **Technical Solution**: Provide Python/pandas code with explanations
6. **Review**: Ensure story flows well and teaches effectively
7. **Publish**: Save to `_posts/` with proper Jekyll filename format

## File Naming Convention

```
YYYY-MM-DD-mystery-{{number}}-{{slug}}.md
```

Example: `2025-08-23-mystery-001-disappearing-dollars.md`

## Categories and Tags

### Standard Categories
- `mysteries` (all posts)
- `reconciliation` (balance/matching issues)
- `data-analysis` (pattern recognition)
- `automation` (efficiency improvements)
- `fraud-detection` (security scenarios)

### Standard Tags
- `pandas` (all posts using pandas)
- `python` (all posts using Python)
- `excel-migration` (moving from Excel)
- `data-cleaning`
- `pattern-matching`
- `rounding-errors`
- `regex`
- `merging`
- `groupby`

## Quality Checklist

### Story Quality
- [ ] Engaging opening that sets the scene
- [ ] Clear problem that readers can relate to
- [ ] Logical investigation flow
- [ ] Satisfying resolution
- [ ] Character voices feel authentic

### Technical Quality
- [ ] Code is functional and tested
- [ ] Comments explain the approach clearly
- [ ] Solution directly addresses story problem
- [ ] Learning points connect story to broader concepts
- [ ] Difficulty level matches content complexity

### Jekyll Integration
- [ ] Proper frontmatter with all required fields
- [ ] Appropriate categories and tags
- [ ] Links to previous/next mysteries work
- [ ] Layout renders correctly
- [ ] Navigation is functional