#!/usr/bin/env python3
"""Verify Jekyll post URL generation against Discord URL logic.

This script compares:
1) Expected Jekyll URL (from _config.yml + filename/front matter)
2) Legacy Discord workflow URL logic (the URLs that were historically posted)
3) Fixed Discord workflow URL logic (current workflow behavior)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Dict, List

import yaml


POST_FILE_PATTERN = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})-(.+)\.(md|html)$")
LEGACY_DISCORD_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|html)$")


@dataclass
class UrlCheckResult:
    filename: str
    expected_url: str
    legacy_discord_url: str
    fixed_discord_url: str
    has_permalink_override: bool

    @property
    def legacy_matches(self) -> bool:
        return self.expected_url == self.legacy_discord_url

    @property
    def fixed_matches(self) -> bool:
        return self.expected_url == self.fixed_discord_url


def read_yaml_front_matter(post_path: Path) -> Dict:
    text = post_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def build_url(site_url: str, baseurl: str, path: str) -> str:
    path = "/" + path.lstrip("/")
    baseurl = (baseurl or "").strip("/")
    if baseurl:
        return f"{site_url.rstrip('/')}/{baseurl}{path}"
    return f"{site_url.rstrip('/')}{path}"


def render_permalink(template: str, date_obj: datetime, slug: str) -> str:
    rendered = template
    rendered = rendered.replace(":year", f"{date_obj.year:04d}")
    rendered = rendered.replace(":month", f"{date_obj.month:02d}")
    rendered = rendered.replace(":day", f"{date_obj.day:02d}")
    rendered = rendered.replace(":title", slug)
    return rendered


def parse_filename(post_path: Path):
    match = POST_FILE_PATTERN.match(post_path.name)
    if not match:
        raise ValueError(f"Unexpected post filename format: {post_path.name}")
    year, month, day, raw_slug, _ = match.groups()
    post_date = datetime(int(year), int(month), int(day))
    return post_date, raw_slug


def expected_url_for_post(post_path: Path, config: Dict) -> str:
    post_date, raw_slug = parse_filename(post_path)
    normalized_slug = slugify(raw_slug)
    front_matter = read_yaml_front_matter(post_path)

    permalink_override = front_matter.get("permalink")
    if permalink_override:
        rendered_path = render_permalink(str(permalink_override), post_date, normalized_slug)
    else:
        permalink_template = config.get("permalink", "/:year-:month-:day-:title/")
        rendered_path = render_permalink(str(permalink_template), post_date, normalized_slug)

    return build_url(config.get("url", ""), config.get("baseurl", ""), rendered_path)


def legacy_discord_url_for_post(post_path: Path) -> str:
    site_root = "https://pandaudit.com"
    match = LEGACY_DISCORD_PATTERN.match(post_path.name)
    if match:
        year, month, day, slug, _ = match.groups()
        return f"{site_root}/{year}/{month}/{day}/{slug}"
    return f"{site_root}/blog"


def fixed_discord_url_for_post(post_path: Path) -> str:
    site_root = "https://pandaudit.com"
    fm = read_yaml_front_matter(post_path)

    permalink = fm.get("permalink")
    if permalink:
        return f"{site_root}/{str(permalink).lstrip('/')}"

    post_date, raw_slug = parse_filename(post_path)
    slug = slugify(raw_slug)
    return f"{site_root}/{post_date.year:04d}-{post_date.month:02d}-{post_date.day:02d}-{slug}/"


def select_sample_posts(posts: List[Path]) -> List[Path]:
    if len(posts) <= 4:
        return posts
    indexes = sorted({0, len(posts) // 3, (2 * len(posts)) // 3, len(posts) - 1})
    return [posts[i] for i in indexes]


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    config = yaml.safe_load((repo_root / "_config.yml").read_text(encoding="utf-8")) or {}
    posts = sorted((repo_root / "_posts").glob("*.md"))

    if not posts:
        print("No posts found under _posts/")
        return 1

    samples = select_sample_posts(posts)
    results: List[UrlCheckResult] = []

    for post in samples:
        fm = read_yaml_front_matter(post)
        results.append(
            UrlCheckResult(
                filename=post.name,
                expected_url=expected_url_for_post(post, config),
                legacy_discord_url=legacy_discord_url_for_post(post),
                fixed_discord_url=fixed_discord_url_for_post(post),
                has_permalink_override=bool(fm.get("permalink")),
            )
        )

    print("Sample URL verification results")
    print("=" * 80)
    for r in results:
        print(f"\nFile: {r.filename}")
        print(f"Expected URL:        {r.expected_url}")
        print(f"Legacy Discord URL:  {r.legacy_discord_url}")
        print(f"Fixed Discord URL:   {r.fixed_discord_url}")
        print(f"Permalink override:  {r.has_permalink_override}")
        print(f"Legacy Match:        {'YES' if r.legacy_matches else 'NO'}")
        print(f"Fixed Match:         {'YES' if r.fixed_matches else 'NO'}")

    legacy_mismatches = [r for r in results if not r.legacy_matches]
    fixed_mismatches = [r for r in results if not r.fixed_matches]

    print("\n" + "=" * 80)
    print(f"Checked {len(results)} sample posts")
    print(f"Legacy mismatches: {len(legacy_mismatches)}")
    print(f"Fixed mismatches: {len(fixed_mismatches)}")

    if fixed_mismatches:
        print("\nFixed-logic mismatch summary:")
        for item in fixed_mismatches:
            print(f"- {item.filename}")
        return 2

    print("\nAll sampled posts match the fixed Discord URL logic.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
