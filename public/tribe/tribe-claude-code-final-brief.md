# Claude Code Brief — Tribe Case Study
## Task: Embed real images · Fix one layout issue · Verify & ship

---

## Context

`tribe-case-study.html` is a complete, working case study for product designer Orsolya Gorcz. Design system, typography, components, JS, and responsive layout are all finished and correct. Do not redesign anything.

**The only jobs:**
1. Embed the 20 real PNG images (currently referenced as flat filenames)
2. Fix one known layout issue (described below)
3. Run the verification checklist
4. Output `tribe-case-study.html` — same filename, in-place

---

## Job 1 — Embed images as base64

Every `<img src="filename.png">` in the file references a flat PNG in the same folder. Convert each to inline base64 so the file is fully self-contained and works without a server.

**All 20 image files to embed:**

```
App_Screen.png                              ← wide landscape, chip validation 9-frame strip
Landing-Signed.png                          ← portrait phone, onboarding splash
Landing-Signed_In_empty_state.png           ← portrait phone, Gen 2 AI metadata tags
Landing-Signed_In_empty_state_collapsed.png ← portrait phone, Gen 1 manual tags
Landing-Signed_In_empty_state_collapseds.png← portrait phone, empty prompt workspace
Landing-Signed_In_filled_state_correct.png  ← portrait phone, validated Gen 3 chips
Landing-processing1.png                     ← portrait phone, processing galactic bg
Leave_chat.png                              ← portrait phone, safety exit modal
Match.png                                   ← portrait phone, match results (in device mockup)
Messaging-Mobile-1.png                      ← portrait phone, AI suggest chat
Messaging-Mobile.png                        ← portrait phone, chat screen
NO_MATCH_FOUND.png                          ← portrait phone, no match fallback
Sprint_1.png                                ← very wide landscape, wireframe sheet
breathe.png                                 ← portrait phone, breathe chat modal
core-happy-path.png                         ← wide landscape, architecture diagram
functional-sitemap.png                      ← very wide landscape, IA sitemap
interaction-gap-matrix.png                  ← landscape, framework document
meethub.png                                 ← portrait phone, meet hub screen
processing_2.png                            ← portrait phone, GPS modal mid-processing
report_user_focus.png                       ← portrait phone, inline report user
```

**How to embed:**
```python
import base64, re

def embed(path):
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"

with open('tribe-case-study.html') as f:
    html = f.read()

images = [
    'App_Screen.png',
    'Landing-Signed.png',
    'Landing-Signed_In_empty_state.png',
    'Landing-Signed_In_empty_state_collapsed.png',
    'Landing-Signed_In_empty_state_collapseds.png',
    'Landing-Signed_In_filled_state_correct.png',
    'Landing-processing1.png',
    'Leave_chat.png',
    'Match.png',
    'Messaging-Mobile-1.png',
    'Messaging-Mobile.png',
    'NO_MATCH_FOUND.png',
    'Sprint_1.png',
    'breathe.png',
    'core-happy-path.png',
    'functional-sitemap.png',
    'interaction-gap-matrix.png',
    'meethub.png',
    'processing_2.png',
    'report_user_focus.png',
]

for img in images:
    try:
        html = html.replace(f'src="{img}"', f'src="{embed(img)}"')
        print(f"✓ {img}")
    except FileNotFoundError:
        print(f"✗ MISSING: {img}")

with open('tribe-case-study.html', 'w') as f:
    f.write(html)
```

**Note on the 3 renamed files** — these were renamed from their original timestamp filenames. If the renamed versions aren't present, check for:
- `interaction-gap-matrix.png` ← was `14_03_2026_19_25_22_REC.png`
- `core-happy-path.png`        ← was `15_03_2026_18_42_06_REC.png`
- `functional-sitemap.png`     ← was `14_03_2026_19_24_47_REC.png`

---

## Job 2 — Fix one layout issue

The `.compare-panels` (Reflection section) uses `grid-template-columns:1fr 1fr` on desktop showing both processing screens side by side. The `.compare-flag` callouts (red annotation labels) on the right panel point left with `left: calc(100% + 10px)` — but at the half-page width the column is too narrow and the flags overflow outside the card.

**Fix:** constrain the flags to render below their anchor point when the panel width is under 300px:

```css
/* Add to existing .compare-flag rule */
.compare-flag {
  /* existing rules stay */
  max-width: 120px;
  word-wrap: break-word;
}

/* Override for narrow columns */
@media (max-width: 900px) {
  .compare-flag {
    position: static;
    transform: none;
    left: auto;
    right: auto;
    width: auto;
    max-width: 100%;
    margin-top: 6px;
    border-left: 2px solid #F0C4C2;
    border-radius: 0 5px 5px 0;
  }
  .compare-flag::before { display: none; }
}
```

---

## Job 3 — Verification checklist

Run these checks before finishing. Every item must pass:

```bash
# 1. No external image references remain
grep 'src="[^d]' tribe-case-study.html | grep -v "data:image" | wc -l
# Expected: 0

# 2. All 20 images embedded
grep -c "data:image/png;base64" tribe-case-study.html
# Expected: 20 or more (some appear twice — Match.png used in device mockup AND flow strip)

# 3. No broken src attributes
grep 'src=""' tribe-case-study.html | wc -l
# Expected: 0

# 4. File is valid HTML (no truncation)
tail -5 tribe-case-study.html
# Expected: closing </script>, </body>, </html> tags present

# 5. Key design tokens present
grep "#F4F1ED\|#6B5F9E\|grain\|topbar.scrolled" tribe-case-study.html | wc -l
# Expected: 4+
```

---

## Do not change

- Any CSS rules
- Any HTML structure or content
- Any JavaScript
- The filename (`tribe-case-study.html`)
- The font import (Plus Jakarta Sans only — no Lora)
- The design system tokens

The file is production-ready except for the missing image embeds and the compare-flag overflow fix. Change nothing else.

---

## File location

All files are in the same flat directory. No subdirectories. The HTML file and all 20 PNGs sit together.
