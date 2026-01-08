# Contributing to PANDAUDIT

Thank you for your interest in contributing to PANDAUDIT! We welcome contributions from the community.

---

## 📋 Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Writing Blog Posts](#writing-blog-posts)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Submission Process](#submission-process)
5. [Community Guidelines](#community-guidelines)

---

## 🤝 Ways to Contribute

### 1. Write Guest Blog Posts

Share your Python automation story! We're always looking for:
- Real-world use cases (accounting, finance, data analysis)
- "How I solved X problem" tutorials
- Tips & tricks for pandas, Python, Excel automation
- Cheat sheets and quick references

### 2. Improve Existing Posts

Found a typo? Have a better code example? Suggestions welcome!
- Fix typos/grammar
- Update outdated code
- Add clarifications
- Improve code examples

### 3. Report Issues

- **Bugs:** Site not loading? Links broken? Report it!
- **Content suggestions:** Topics you want to see covered
- **Improvements:** Design, UX, performance suggestions

### 4. Share Your Wins

Used code from PANDAUDIT and saved hours? Share your story!
- Discord `#showcase` channel
- Guest post opportunity
- Community spotlight

---

## ✍️ Writing Blog Posts

### Post Format

**1. File Naming:**
```
_posts/YYYY-MM-DD-title-slug.md
```
Example: `_posts/2026-01-25-automate-month-end-close.md`

**2. Front Matter:**
```yaml
---
layout: primer_post
title: "Your Compelling Title (50-70 characters)"
subtitle: "Hook readers in one sentence (100-150 characters)"
tags: [python, pandas, automation, accounting, finance]
comments: true
author: Your Name
---
```

**3. Post Structure:**

```markdown
## The Problem (Hook)

Start with a relatable pain point. Example:
"You spent 4 hours creating pivot tables for month-end close? There's a better way."

---

## Why This Matters

Explain the business context. Why should accountants care?

---

## The Solution

### Step 1: [Clear action]

```python
# Well-commented code
import pandas as pd

df = pd.read_excel('trial_balance.xlsx')
# More code...
```

**Explanation:** [What this code does, why it's elegant]

### Step 2: [Next action]

[Continue...]

---

## Real-World Example

Show the complete workflow with realistic data (sanitized).

---

## Time Savings

| Method | Time |
|--------|------|
| Excel Manual | 4 hours |
| Python Automated | 2 minutes |

---

## Try It Yourself!

Provide downloadable sample data or complete script.

---

## What's Next?

Link to 2-3 related posts.

---

## Your Turn!

Ask a question to encourage comments and engagement.
```

### Writing Guidelines

**DO:**
- ✅ Start with a relatable problem
- ✅ Use real-world examples (sanitize sensitive data)
- ✅ Include complete, working code
- ✅ Add comments explaining *why*, not just *what*
- ✅ Show before/after comparisons (Excel vs Python)
- ✅ Include time savings or ROI
- ✅ Link to related posts
- ✅ End with a question or call-to-action

**DON'T:**
- ❌ Assume readers know programming jargon
- ❌ Show code without explanation
- ❌ Use overly complex examples for beginners
- ❌ Skip error handling in production code
- ❌ Forget to cite external resources
- ❌ Include real company/client data (even if public)

### Code Standards

**Python Code:**
```python
import pandas as pd  # Standard imports first
import numpy as np

# Use descriptive variable names
trial_balance_df = pd.read_excel('trial_balance.xlsx')

# Add comments for complex logic
# Calculate fiscal quarter (July-June fiscal year)
tb_df['fiscal_quarter'] = pd.PeriodIndex(
    tb_df['date'], 
    freq='Q-JUN'
).strftime('Q%q')

# Use proper spacing and formatting (PEP 8)
def calculate_annual_amount(payment, frequency):
    """
    Convert payment to annual amount.
    
    Args:
        payment (float): Payment amount per period
        frequency (str): Payment frequency ('Monthly', 'Bi-Weekly', etc.)
    
    Returns:
        float: Annualized amount
    """
    multipliers = {
        'Monthly': 12,
        'Bi-Weekly': 26,
        'Weekly': 52
    }
    return payment * multipliers.get(frequency, 12)
```

**Code Formatting:**
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 79 characters (PEP 8)
- Add docstrings to functions
- Use type hints for clarity (optional but encouraged)

---

## 📝 Submission Process

### For Blog Posts

**Option 1: GitHub Pull Request (Preferred)**

1. Fork the repository
2. Create new branch: `git checkout -b new-post-title`
3. Add your post to `_posts/` directory
4. Test locally: `bundle exec jekyll serve`
5. Commit: `git commit -m "Add post: Your Title"`
6. Push: `git push origin new-post-title`
7. Open Pull Request with description:
   ```
   ## New Post: [Your Title]
   
   **Summary:** [2-3 sentence description]
   
   **Target Audience:** [e.g., Intermediate accountants learning pandas]
   
   **Key Takeaways:**
   - Takeaway 1
   - Takeaway 2
   
   **Checklist:**
   - [x] Post follows formatting guidelines
   - [x] Code tested and works
   - [x] Links to related posts included
   - [x] Tags added
   ```

**Option 2: Email Submission**

Email to: hello@pandaudit.com

**Subject:** Guest Post Submission: [Your Title]

**Body:**
- Attach Markdown file (.md)
- Include author bio (2-3 sentences)
- Links to your website/LinkedIn (optional)
- Any images/screenshots

### For Bug Reports

Open GitHub Issue with:

**Title:** [BUG] Clear description

**Template:**
```
**Description:**
[Clear description of the bug]

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. See error

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshots:**
[If applicable]

**Browser/Device:**
- Browser: [e.g., Chrome 120]
- Device: [e.g., Desktop, iPhone]
- OS: [e.g., Windows 11, iOS 17]
```

### For Feature Requests

Open GitHub Issue with:

**Title:** [FEATURE] Your suggestion

**Template:**
```
**Problem:**
[What problem does this solve?]

**Proposed Solution:**
[How would you solve it?]

**Alternatives Considered:**
[Other approaches?]

**Additional Context:**
[Screenshots, examples, links]
```

---

## 🎨 Design Guidelines

### Visual Elements

**Code Screenshots:**
- Use [Carbon](https://carbon.now.sh/) for beautiful code images
- Theme: Dracula or One Dark
- Font: Fira Code
- Include comments in screenshots

**Diagrams:**
- Use [Excalidraw](https://excalidraw.com/) for hand-drawn style
- Keep it simple and clear
- Export as PNG (2x resolution)

**Before/After Comparisons:**
- Side-by-side when possible
- Use screenshots or tables
- Highlight key differences

---

## 👥 Community Guidelines

### Code of Conduct

1. **Be Respectful** - Treat everyone with respect and kindness
2. **Be Helpful** - Share knowledge, don't gatekeep
3. **Be Professional** - Remember this is a professional community
4. **Give Credit** - Cite sources, acknowledge contributions
5. **Stay On Topic** - Finance, accounting, Python, data analytics

### What's Not Allowed

- ❌ Spam or self-promotion (unless in designated areas)
- ❌ Harassment or discriminatory behavior
- ❌ Sharing proprietary/confidential information
- ❌ Plagiarism
- ❌ Off-topic discussions

### Moderation

- First offense: Warning
- Second offense: Temporary ban
- Third offense: Permanent ban

Moderators have final say. Contact hello@pandaudit.com to appeal.

---

## 🎁 Recognition

### For Contributors

**Guest Authors:**
- Byline on your post
- Bio with link to your website/LinkedIn
- Promoted on social media (LinkedIn, Twitter, Discord)
- Added to Contributors list

**Code Contributors:**
- Listed in Contributors section of README
- Mentioned in release notes

**Community Helpers:**
- Special Discord role: `@Helper`
- Monthly "Member Spotlight"
- Potential moderator opportunities

---

## 📧 Questions?

**Not sure if your idea fits?** Reach out!

- **Email:** hello@pandaudit.com
- **Discord:** #general channel
- **GitHub:** Open a discussion

We're friendly and want to help you contribute!

---

## ✅ Contributor Checklist

Before submitting, ensure:

- [ ] Post follows formatting guidelines
- [ ] Code is tested and works
- [ ] No sensitive/proprietary data included
- [ ] All code is properly commented
- [ ] Links to related posts added
- [ ] Images optimized (<1MB each)
- [ ] Tags added (3-7 tags)
- [ ] Author bio provided (if guest post)
- [ ] Tested locally (if possible)
- [ ] Pull request description complete

---

**Thank you for contributing to PANDAUDIT!** 🎉

Together, we're helping accountants and finance professionals escape Excel hell and embrace Python automation.

[Back to README](README.md)
