import re

with open('ref_html/index-html.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

rules = {}
for m in re.finditer(r'\.([a-zA-Z0-9_]+)\s*\{([^}]+)\}', text):
    rules[m.group(1)] = m.group(2)

pages = re.split(r'<div id="page\d+-div"', text)
with open('full_ref_analysis.txt', 'w', encoding='utf-8') as out:
    for i in range(1, len(pages)):
        out.write(f"\n==================== PAGE {i} ====================\n")
        elems = re.findall(r'<p style="position:absolute;top:(\d+)px;left:(\d+)px[^"]*" class="([^"]+)">(.*?)</p>', pages[i])
        for top, left, cls, val in elems:
            clean = re.sub(r'<[^>]+>', ' ', val).strip().replace('&#160;', ' ')
            clean = re.sub(r'\s+', ' ', clean)
            style = rules.get(cls, '')
            font_size = re.search(r'font-size:(\d+px)', style)
            fs = font_size.group(1) if font_size else ''
            font_family = re.search(r'font-family:([^;]+)', style)
            ff = font_family.group(1).split('+')[-1] if font_family else ''
            color = re.search(r'color:([^;]+)', style)
            c = color.group(1) if color else ''
            out.write(f"[y={top:>4}, x={left:>4}] sz={fs:>4} {c:>7} {ff[:22]:<22} | {clean}\n")
print("Dumped successfully!")
