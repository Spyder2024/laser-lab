import re

with open('ref_html/index-html.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Get CSS styles
styles = dict(re.findall(r'\.([a-zA-Z0-9]+)\{([^}]+)\}', content))

page_splits = re.split(r'<div id="page(\d+)-div"', content)

for i in range(1, len(page_splits), 2):
    p_num = page_splits[i]
    chunk = page_splits[i+1].split('</div>\n</div>')[0]
    print(f"\n=================== PAGE {p_num} ===================")
    paras = re.findall(r'<p[^>]*class="([^"]+)"[^>]*style="([^"]+)"[^>]*>(.*?)</p>', chunk)
    for cls, style, text in paras[:40]:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        css = styles.get(cls, '')
        # extract font-size and color
        sz = re.search(r'font-size:([^;]+)', css)
        sz_str = sz.group(1) if sz else ''
        col = re.search(r'color:([^;]+)', css)
        col_str = col.group(1) if col else ''
        ff = re.search(r'font-family:([^;]+)', css)
        ff_str = ff.group(1).split('+')[-1] if ff else ''
        top = re.search(r'top:(\d+)px', style)
        left = re.search(r'left:(\d+)px', style)
        t_val = top.group(1) if top else ''
        l_val = left.group(1) if left else ''
        if clean:
            print(f"[{l_val:>4}, {t_val:>4}] sz={sz_str:>4} {col_str:>7} {ff_str:<25} | {clean[:60]}")
