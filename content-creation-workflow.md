# Content Creation Workflow - Masha & Panda Mysteries

*The systematic "Real-to-Mystery" process for turning accounting scenarios into engaging educational content.*

## Overview

This workflow transforms real accounting challenges into story-driven learning experiences using the Masha & Panda detective mystery format. The system emphasizes efficiency, authenticity, and educational value.

## The 3-Phase Workflow

### PHASE 1: CAPTURE (Hybrid Approach)
*Immediate capture + weekly batch processing*

#### Immediate Capture (30 seconds)
- **When**: Encountering interesting scenarios during real work
- **How**: Quick bullet point in `mystery-ideas.md`
- **Format**: `- [ ] Brief description + key challenge`
- **Examples**: 
 - `- [ ] Subledger off by $0.17 - took 2 hours to find rounding difference`
 - `- [ ] Regex nightmare extracting data from 50 legacy CSV files`

#### Weekly Batch Processing (30 minutes)
- **When**: Weekly scheduled session (recommend Friday afternoon)
- **Process**: Review quick captures, select 2-3 for development
- **Output**: Detailed story outlines with character moments
- **Goal**: Build development queue for future mysteries

### PHASE 2: STRUCTURE (Linear Story Format)
*Simple Jekyll blog post approach*

#### Story Framework
1. **Opening** (2-3 paragraphs)
 - Set the scene: normal workday, routine task
 - Introduce the problem: something doesn't add up

2. **Investigation** (3-4 paragraphs)
 - Walk through manual checking process
 - Show growing confusion or frustration
 - Include dead ends and false leads

3. **Character Commentary** (throughout story)
 - **Masha**: Practical frustration, pattern recognition
 - **Panda**: Alternative perspectives, gentle guidance
 - **Format**: Markdown blockquotes with character names

4. **Resolution** (2-3 paragraphs)
 - The breakthrough moment
 - How the real solution was discovered
 - Satisfaction of problem solved

5. **Technical Solution** (separate section)
 - Complete Python/pandas code
 - Clear comments explaining approach
 - Directly solves the story problem

### PHASE 3: JEKYLL TEMPLATE (Mystery Series)
*Consistent professional format*

#### Template Usage
1. **Copy Template**: Use `_includes/mystery-template.md`
2. **Fill Frontmatter**: All required Jekyll fields
3. **Replace Content**: Story, characters, code, learning points
4. **Review Quality**: Story flow, technical accuracy, engagement
5. **Publish**: Save to `_posts/` with proper naming

#### Naming Convention
`YYYY-MM-DD-mystery-###-slug.md`

Example: `2025-08-23-mystery-001-disappearing-dollars.md`

## 30-Minute Weekly Session Structure

### Minutes 1-5: Review & Select
- Review quick captures from the week
- Select 2-3 most engaging scenarios
- Consider difficulty level and teaching value

### Minutes 6-15: Outline Development
- For each selected scenario:
 - Identify story beats (problem → investigation → resolution)
 - Plan character commentary moments
 - Note technical solution approach

### Minutes 16-25: First Mystery Draft
- Choose one outline to develop
- Write story structure using template
- Plan character dialogue and technical solution

### Minutes 26-30: Queue Management
- Update mystery-ideas.md with outlines
- Move completed mysteries to "done" section
- Plan next week's development priorities

## Quality Standards

### Story Engagement
- **Authentic**: Based on real workplace scenarios
- **Relatable**: Problems readers have experienced
- **Progressive**: Investigation builds logically
- **Satisfying**: Resolution feels earned

### Educational Value
- **Practical**: Code solves real problems
- **Transferable**: Techniques apply to other scenarios
- **Accessible**: Appropriate for skill level
- **Memorable**: Characters make concepts stick

### Technical Quality
- **Functional**: All code runs correctly
- **Commented**: Explanations are clear
- **Complete**: Full solution provided
- **Tested**: Verified to work as shown

## Tools & Resources

### Required Files
- `mystery-ideas.md` - Capture and development queue
- `_includes/mystery-template.md` - Content template
- `docs/mystery-template-guide.md` - Detailed usage guide

### Jekyll Structure
- `_layouts/mystery.html` - Post layout
- `_posts/YYYY-MM-DD-mystery-###-title.md` - Published mysteries
- Categories: mysteries, topic-area
- Tags: pandas, python, specific-techniques

### Development Environment
- Text editor with Markdown support
- Python environment for testing code
- Jekyll for local preview (optional)

## Success Metrics

### Efficiency Indicators
- **Time to Capture**: < 30 seconds per scenario
- **Weekly Session**: Complete in 30 minutes
- **Template Usage**: < 5 minutes to set up new mystery

### Quality Indicators
- **Story Flow**: Engaging from start to finish
- **Character Voice**: Consistent personality
- **Technical Accuracy**: Code works as shown
- **Educational Impact**: Clear learning outcomes

### Content Pipeline
- **Capture Rate**: 2-3 scenarios per week
- **Development Rate**: 1 mystery per week
- **Quality Rate**: 90% of mysteries meet all standards

## Common Pitfalls & Solutions

### Pitfall: Over-Complicating Stories
- **Solution**: Keep focus on single core problem
- **Prevention**: Use linear structure, avoid branching

### Pitfall: Technical Code Doesn't Match Story
- **Solution**: Write story first, then create exact matching code
- **Prevention**: Test code with story scenario data

### Pitfall: Character Voices Feel Forced
- **Solution**: Read dialogue out loud, ensure natural flow
- **Prevention**: Limit to 2-3 character moments per mystery

### Pitfall: Weekly Sessions Take Too Long
- **Solution**: Use timer, focus on outlines not full drafts
- **Prevention**: Keep quick captures very brief

## Advanced Tips

### Seasonal Content Planning
- **Month-end**: Reconciliation mysteries
- **Year-end**: Complex reporting scenarios 
- **Audit season**: Fraud detection themes
- **Budget season**: Variance analysis mysteries

### Character Development
- **Masha Growth**: Gradually more sophisticated in pattern recognition
- **Panda Wisdom**: Increasingly helpful technical guidance
- **Relationship**: Build partnership over mystery series

### Reader Engagement
- **Callback References**: Link to previous mysteries
- **Difficulty Progression**: Build skills over time
- **Real-world Connection**: Always tie to actual work scenarios