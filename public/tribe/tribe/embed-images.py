#!/usr/bin/env python3
import base64, re, os, sys

SRC = 'tribe-case-study-final.html'
OUT = 'tribe-case-study-final.html'

if not os.path.exists(SRC):
    print(f"ERROR: {SRC} not found in {os.getcwd()}")
    sys.exit(1)

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

IMAGES = [
    'App_Screen.png',
    'Functional_Sitemap___User_Flow_Hybrid_method.png',
    'Human-AI_Interaction_gap_design_solutions.png',
    'Landing-Signed.png',
    'Landing-Signed_In_activated_input_keyboard_32.png',
    'Landing-Signed_In_activated_input_keyboard_40.png',
    'Landing-Signed_In_activated_input_keyboard_48.png',
    'Landing-Signed_In_empty_state_collapseds.png',
    'Landing-Signed_In_empty_state_opened_gen1.png',
    'Landing-Signed_In_empty_state_opened_gen2.png',
    'Landing-processing1.png',
    'Leave_chat.png',
    'Match.png',
    'Messaging-Mobile-1.png',
    'Messaging-Mobile.png',
    'NO_MATCH_FOUND-1.png',
    'NO_MATCH_FOUND.png',
    'Property_1_3chip_smile.png',
    'Sprint_1.png',
    'breathe_chat.png',
    'happypath_fallback.png',
    'landing_empty_no_account_teachable_inputs.png',
    'meethub.png',
    'more_menu_opened.png',
    'processing_2.png',
    'report_user_focus.png',
]

ok = 0
missing = []

for img in IMAGES:
    if not os.path.exists(img):
        missing.append(img)
        print(f"✗ MISSING: {img}")
        continue
    with open(img, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    data_uri = f"data:image/png;base64,{b64}"
    count = html.count(f'src="{img}"')
    if count > 0:
        html = html.replace(f'src="{img}"', f'src="{data_uri}"')
        print(f"✓ {img} ({count} occurrence{'s' if count > 1 else ''})")
        ok += 1
    else:
        print(f"? {img} — not referenced in HTML (skipped)")

# Fix compare-flag overflow on narrow screens
# Flags point left with absolute positioning — breaks on narrow columns
old_flag = """.compare-flag{position:absolute;right:calc(100% + 10px);width:130px;font-size:10px;color:#8B2020;background:#FBE9E8;border:1px solid #F0C4C2;padding:5px 8px;border-radius:6px;line-height:1.4;transform:translateY(-50%)}"""
new_flag = """.compare-flag{position:absolute;right:calc(100% + 10px);width:130px;font-size:10px;color:#8B2020;background:#FBE9E8;border:1px solid #F0C4C2;padding:5px 8px;border-radius:6px;line-height:1.4;transform:translateY(-50%);word-wrap:break-word}"""
if old_flag in html:
    html = html.replace(old_flag, new_flag)
    print("✓ compare-flag CSS fixed")

# Add responsive fallback for compare flags on narrow screens
# Insert before closing </style>
responsive_flag = """
@media(max-width:900px){
  .compare-flag{position:static;transform:none;right:auto;width:auto;max-width:100%;margin-top:6px;border-left:2px solid #F0C4C2;border-radius:0 5px 5px 0}
  .compare-flag::before{display:none}
}"""
if responsive_flag not in html and '</style>' in html:
    html = html.replace('</style>', responsive_flag + '\n</style>', 1)
    print("✓ compare-flag responsive added")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
remaining = re.findall(r'src="(?!data:)[^"]+\.png"', html)
b64_count = len(re.findall(r'src="data:image/png', html))
file_kb = len(html.encode()) // 1024

print(f"\n{'='*50}")
print(f"DONE")
print(f"{'='*50}")
print(f"  Images embedded:   {ok}")
print(f"  Missing:           {len(missing)}")
print(f"  base64 in file:    {b64_count}")
print(f"  Unreplaced srcs:   {len(remaining)}")
print(f"  Output file size:  {file_kb} KB")
print()
if remaining:
    print("  STILL UNREPLACED:")
    for r in remaining:
        print(f"    {r}")
if missing:
    print("  MISSING FILES:")
    for m in missing:
        print(f"    {m}")
if not remaining and not missing:
    print("  ✓ All images embedded — file is self-contained")

# Check file ends correctly
last = html.strip()[-50:]
if '</html>' in last:
    print("  ✓ File ends correctly")
else:
    print("  ✗ WARNING: file may be truncated")
    print(f"    Last 50 chars: {repr(last)}")
