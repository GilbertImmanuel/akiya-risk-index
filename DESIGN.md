# Design

## Theme

A statistical atlas for a desk reader. Cool survey paper, deep ink, one vermilion accent, and ruled columns. The map carries the color; the page around it stays quiet. No cards, no shadows, no marketing hero.

## Color

UI tokens use OKLCH. Map classes use hex because they are also applied directly to Leaflet layer styles.

| Token | Value | Use |
|---|---|---|
| `--bg` | `oklch(93% 0.012 225)` | Page background, cool survey paper |
| `--surface` | `oklch(98.5% 0.004 225)` | Map frame, side panel |
| `--ink` | `oklch(25% 0.025 240)` | Body text, headings |
| `--muted` | `oklch(48% 0.02 235)` | Secondary text, notes |
| `--rule` | `oklch(82% 0.012 230)` | Borders and dividers |
| `--accent` | `oklch(48% 0.13 32)` | Selection, focus, key marks |
| `--link` | `oklch(48% 0.08 230)` | Links |

Map palettes:

| Metric | Colors |
|---|---|
| Dilapidated rate | `#F2E6E2` `#E3B9B0` `#D18778` `#B95645` `#8C2F25` |
| Total vacancy | `#F2E6E2` `#E8C4BB` `#D89484` `#BE5F4D` `#8C2F25` |
| Dilapidated change | `#2C6C8A` `#8FB3C4` `#E8EDF0` `#D89A8A` `#A63A2B` |
| Population change | `#A63A2B` `#D89A8A` `#E8EDF0` `#8FB3C4` `#2C6C8A` |
| Fiscal strength | `#E4EFEC` `#B7D6D0` `#7FB5AA` `#4A8C80` `#245E55` |
| Station density | `#D8DEE2` `#E4EEF3` `#BCD5E2` `#84B0C7` `#4D86A6` `#245F7E` |
| No data | `#B9C2C8` |

## Typography

- Display: **IBM Plex Serif** 400/600, fallback Yu Mincho, Hiragino Mincho ProN, Georgia.
- UI and body: **IBM Plex Sans** 400/500/600, fallback Yu Gothic, Hiragino Kaku Gothic ProN, Segoe UI.
- Base 16px. Headings 2.25rem, 1.5rem, 1.125rem. Body line-height 1.55. Headings 1.2.
- Tabular numerals for all data.
- Sentence case everywhere. No tiny all-caps labels. No Inter.

## Layout

- Max width 1500px, 24px page padding.
- Desktop: map column `minmax(0, 1fr)` plus a 360px side panel, 24px gap.
- Map height `calc(100vh - 190px)`, minimum 560px. Side panel sticky at 24px.
- Mobile: one column, map 60vh, panel below.
- Structural rules, not cards. A 1px rule separates the map and panel.

## Components

- **Metric select:** native select, 44px tall, 1px rule, surface background, accent focus ring.
- **Legend:** 18 × 12px swatches, sentence-case labels, one row per class.
- **Rank rows:** full-width buttons with a bottom rule; hover and focus show a tinted background.
- **Tooltip:** ink background, white text, no arrow; 240px maximum.
- **Popup:** surface background, 1px rule, compact six-row table, small shadow.
- **Reset and reload:** 44px text buttons with a 1px rule.
- **Loading and error:** plain text in the map frame, with a reload button on error.
- **Coverage note:** muted text at the bottom of the panel, not a modal.

## Motion

- Map fill transition 180ms ease-out on metric change.
- Fly-to 500ms; 0ms under `prefers-reduced-motion: reduce`.
- No page-load reveals, no decorative motion.
- Hover and focus changes are immediate.
