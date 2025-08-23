---
layout: page
title: Masha & Panda Mysteries
subtitle: Learn Python & pandas through accounting detective stories
---

Welcome to the **Masha & Panda Mystery Series** - where real accounting challenges become engaging detective stories that teach you Python and pandas skills!

## Meet the Characters

**Masha** 🔍 - The sharp-eyed analyst who gets frustrated with manual work but always spots the patterns. She represents your inner voice wanting efficiency and automation.

**Panda** 🐼 - The wise technical guide who offers different perspectives and gentle guidance. He helps you see problems from new angles without intimidation.

## The Mysteries

{% for post in site.categories.mysteries %}
<div class="mystery-preview">
  <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
  <p class="mystery-meta">
    <span class="mystery-number">Mystery #{{ post.mystery_number }}</span> | 
    <span class="difficulty">{{ post.difficulty_level | capitalize }}</span> | 
    <span class="time">{{ post.estimated_time }}</span>
  </p>
  <p class="mystery-excerpt">{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
  <p class="mystery-skills">
    <strong>Skills:</strong> 
    {% for skill in post.skills_covered %}
      <span class="skill-tag">{{ skill }}</span>{% unless forloop.last %}, {% endunless %}
    {% endfor %}
  </p>
</div>
<hr>
{% endfor %}

## How It Works

Each mystery follows the same engaging format:

1. **The Case** - A real accounting scenario that sets up the problem
2. **Investigation** - Follow the detective work with Masha & Panda commentary  
3. **The Solution** - Complete Python/pandas code that solves the mystery
4. **Key Learning Points** - Takeaways you can apply immediately

All mysteries are based on real accounting scenarios, so you'll learn techniques you can actually use in your work!

---

*New mysteries are added regularly. Check back often for more accounting adventures!*