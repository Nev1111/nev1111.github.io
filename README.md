# PANDAUDIT - Python Data Analytics for Finance and Accounting

[![GitHub Pages](https://img.shields.io/badge/Live-pandaudit.com-blue)](https://pandaudit.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?label=Discord&logo=discord)](https://discord.gg/hDQKM6ar)

**Transform Excel nightmares into automated Python workflows.** Real-world examples from government pension fund accounting.

---

### What is PANDAUDIT?

PANDAUDIT is a blog and community for **finance and accounting professionals** who want to:
- Automate repetitive Excel tasks
- Learn Python without a computer science degree
- Save hours every week on manual data processing
- Advance their careers with modern data skills

#### Why PANDAUDIT is Different

- **Real-World Focus** - Actual government pension fund code, not toy examples 
- **Accounting-First** - Written by accountants, for accountants 
- **Immediate ROI** - Save hours this week, not after a 6-month course 
- **Community Support** - Discord for help from fellow finance professionals

---

### Popular Topics

- **From Excel Hell to Python Heaven** - Parse legacy reports, handle credit/debit notation, automate pivots
- **Data Integration and Quality** - Master data mapping, multi-year consolidation, SQL integration
- **Advanced Techniques** - Groupby transforms, data reshaping, duplicate handling
- **Complete Workflows** - End-to-end automation examples

---

### Getting Started

#### For Readers

1. **Browse the Blog:** [pandaudit.com/blog](https://pandaudit.com/blog)
2. **Join Discord:** [discord.gg/hDQKM6ar](https://discord.gg/hDQKM6ar)
3. **Subscribe:** Get new posts via [RSS](/feed.xml)

#### For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to:
- Submit new blog posts
- Report issues or suggest improvements
- Contribute code examples

---

### Technology Stack

**Frontend:**
- [Primer CSS](https://primer.style/) - GitHub's design system
- Jekyll - Static site generator
- GitHub Pages - Hosting

**Automation:**
- GitHub Actions - Discord notifications for new posts
- Python/Pandas - All code examples

---

### Site Structure

```
├── _posts/ # Blog posts (Markdown)
├── _layouts/ # Page templates
│ ├── primer_base.html
│ ├── primer_home.html
│ ├── primer_post.html
│ └── primer_default.html
├── _includes/ # Reusable components
│ ├── primer_nav.html
│ └── primer_footer.html
├── assets/
│ ├── css/ # Custom styles
│ └── img/ # Images
├── .github/
│ └── workflows/ # GitHub Actions
│ └── discord-notify.yml
├── _config.yml # Site configuration
├── blog.html # Blog listing page
├── index.md # Homepage
├── aboutme.md # About page
├── cheatsheet.md # Python cheat sheet
└── stories.md # Mystery stories
```

---

### Design System

PANDAUDIT uses [Primer CSS](https://primer.style/) for a clean, professional look.

**Custom Branding:**
- Primary: `#008AFF` (blue)
- Hover: `#0085A1` (teal)
- Background: `#EAEAEA` (light gray)
- Text: `#404040` (dark gray)

---

### Writing Blog Posts

#### Create a New Post

1. Create file in `_posts/` with format: `YYYY-MM-DD-title-slug.md`
2. Add front matter:

```yaml
---
layout: primer_post
title: "Your Post Title"
subtitle: "Brief description that hooks readers"
tags: [python, pandas, accounting, automation]
comments: true
author: PANDAUDIT Team
---
```

3. Write content in Markdown
4. Commit and push to `master` branch
5. GitHub Pages will build and deploy automatically
6. Discord notification sent automatically (if webhook configured)

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed writing guidelines.

---

### Discord Integration

Automatic notifications for new blog posts.

**Setup:**
1. Create Discord webhook (Server Settings, Integrations, Webhooks)
2. Add webhook URL to GitHub Secrets as `DISCORD_WEBHOOK_URL`
3. Push new post to `master` branch
4. GitHub Actions triggers and posts to Discord automatically

See [DISCORD_SETUP.md](DISCORD_SETUP.md) for complete setup guide.

---

### Marketing and Growth

Want to grow your audience? See [MARKETING_GUIDE.md](MARKETING_GUIDE.md) for:
- Social media strategies (LinkedIn, Reddit, Twitter)
- Content distribution playbook
- Community building tips
- 90-day launch plan
- SEO optimization

---

### Local Development

#### Prerequisites

- Ruby 2.7+
- Bundler
- Jekyll

#### Setup

```bash
# Clone repository
git clone https://github.com/nev1111/nev1111.github.io.git
cd nev1111.github.io

# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# Open in browser
http://localhost:4000
```

**Note:** Localhost refers to the development machine, not your local computer. See deployment instructions for accessing remotely.

---

### Deployment

Site is automatically deployed via GitHub Pages when you push to `master` branch.

**Custom Domain:**
- Domain: `pandaudit.com`
- CNAME file in repository root
- DNS configured with A records pointing to GitHub Pages

---

### License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Content License:** Blog posts and content are copyright 2024 PANDAUDIT. Code examples in posts are MIT licensed.

---

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Writing guidelines
- Code style
- Submission process
- Community standards

---

### Contact

- **Website:** [pandaudit.com](https://pandaudit.com)
- **Email:** hello@pandaudit.com
- **Discord:** [discord.gg/hDQKM6ar](https://discord.gg/hDQKM6ar)
- **Twitter:** Coming soon
- **LinkedIn:** Coming soon

---

### Acknowledgments

- **Primer CSS** by GitHub - Beautiful, accessible design system
- **Jekyll** - Static site generator
- **GitHub Pages** - Free hosting
- **Beautiful Jekyll** - Original theme inspiration (migrated to Primer CSS)
- **Community** - All the accountants sharing their Excel pain points

---

### Stats

- **Blog Posts:** 28+ (and growing)
- **Topics Covered:** Excel automation, pandas, data wrangling, fiscal calculations, reporting
- **Community:** Join our growing Discord community

---

### Roadmap

**Q1 2026:**
- [x] Migrate to Primer CSS design system
- [x] Create comprehensive blog post series
- [x] Set up Discord integration
- [ ] Launch email newsletter
- [ ] Reach 1,000 Discord members

**Q2 2026:**
- [ ] Video tutorials (YouTube channel)
- [ ] Interactive Jupyter notebooks
- [ ] "Python for Accountants" course
- [ ] Community showcase section

**Q3 2026:**
- [ ] Webinars and workshops
- [ ] Corporate training program
- [ ] Mobile-optimized experience
- [ ] Multi-language support

---

**Star this repo if you find it helpful!**

**Join the community and start automating your workflows today!**

[Visit PANDAUDIT](https://pandaudit.com)
