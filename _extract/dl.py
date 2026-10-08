import os, ssl, sys, urllib.request

OUT = r'C:\Users\Admin\Desktop\公差配合实训\_extract'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
      'Referer': 'https://www.renrendoc.com/paper/231824760.html'}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HASH = '74997829c1a6abf71b8a2eda2e04bade'
targets = []
for n in (27, 28, 29, 30, 31, 32):
    targets.append((f'slide{n}.gif', f'https://file4.renrendoc.com/view/{HASH}/{HASH}{n}.gif'))
targets.append(('xypi_gauge.pdf', 'https://jwc.xypi.edu.cn/__local/0/6B/A5/172001EBAFFC2876FDEF3EF7B3F_4F4B40F9_99409F.pdf'))

for name, url in targets:
    dst = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
            data = r.read()
        with open(dst, 'wb') as f:
            f.write(data)
        head = data[:8]
        print(f'OK   {name:20s} {len(data):>9d} bytes  head={head!r}')
    except Exception as e:
        print(f'FAIL {name:20s} {type(e).__name__}: {e}')
