"""Mã hóa trang gửi khách bằng mật khẩu (AES-256-GCM, khóa sinh bằng PBKDF2-SHA256).

Dùng:  python3 tools/encrypt_page.py <trang_goc.html> <mat_khau> public/index.html
Trang gốc (chưa mã hóa) KHÔNG commit vào repo; chỉ commit public/index.html đã mã hóa.
"""
import base64, os, re, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 300_000
src, password, out = sys.argv[1], sys.argv[2], sys.argv[3]
html = open(src, encoding='utf-8').read()
# Bỏ màn khóa cũ (chỉ chặn phía trình duyệt) vì đã có lớp mã hóa thật
html = html.replace('<body class="locked">', '<body>', 1)
html = re.sub(r'<div id="gate">.*?</div>\s*</form>\s*</div>|<div id="gate">\s*<form.*?</form>\s*</div>', '', html, count=1, flags=re.S)
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(password.encode())
ct = AESGCM(key).encrypt(iv, html.encode('utf-8'), None)
b = lambda x: base64.b64encode(x).decode()
page = f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Mai Linh Social – Tài liệu dự án</title>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6f8f5;--card:#fff;--ink:#14201a;--muted:#5b6b61;--line:#dfe7e0;--brand:#0f8a43;--soft:#e2f4e8;--err:#c2410c}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0d1410;--card:#141d18;--ink:#e8efe9;--muted:#9fb0a5;--line:#24342b;--brand:#2fbf6b;--soft:#173825;--err:#fb923c}}}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--ink);font:16px/1.6 "Be Vietnam Pro",system-ui,sans-serif;padding:16px}}
form{{width:100%;max-width:400px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:28px;box-shadow:0 8px 24px rgba(0,0,0,.06)}}
.tag{{display:inline-block;font-size:12px;font-weight:600;color:var(--brand);background:var(--soft);padding:3px 10px;border-radius:99px;margin-bottom:12px}}
h1{{font-size:20px;margin:0 0 4px}}p{{color:var(--muted);font-size:14px;margin:0 0 18px}}
input{{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font:inherit}}
button{{margin-top:12px;width:100%;padding:12px;border:0;border-radius:10px;background:var(--brand);color:#fff;font:600 15px "Be Vietnam Pro",sans-serif;cursor:pointer}}
button[disabled]{{opacity:.6;cursor:wait}}.err{{color:var(--err);font-size:13px;min-height:20px;margin-top:8px}}
</style></head><body>
<form id="f"><div class="tag">Tài liệu tổng quan &amp; khái toán sơ bộ</div>
<h1>Mai Linh Social – Hệ sinh thái Mạng xã hội Taxi Web3</h1>
<p>Kính gửi anh John Davis. Vui lòng nhập mật khẩu được cung cấp để xem tài liệu.</p>
<input id="pw" type="password" placeholder="Mật khẩu" autocomplete="current-password" autofocus>
<button id="b" type="submit">Xem tài liệu</button><div class="err" id="e"></div></form>
<script>
const D={{s:"{b(salt)}",i:"{b(iv)}",c:"{b(ct)}",n:{ITER}}};
const u=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function dec(pw){{
  const base=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']);
  const key=await crypto.subtle.deriveKey({{name:'PBKDF2',salt:u(D.s),iterations:D.n,hash:'SHA-256'}},base,{{name:'AES-GCM',length:256}},false,['decrypt']);
  return new TextDecoder().decode(await crypto.subtle.decrypt({{name:'AES-GCM',iv:u(D.i)}},key,u(D.c)));
}}
function show(html){{document.open();document.write(html);document.close();}}
document.getElementById('f').addEventListener('submit',async ev=>{{
  ev.preventDefault();const e=document.getElementById('e'),b=document.getElementById('b');
  if(!window.crypto||!crypto.subtle){{e.textContent='Trình duyệt không hỗ trợ. Vui lòng mở bằng Chrome, Edge hoặc Safari bản mới.';return}}
  b.disabled=true;b.textContent='Đang mở…';
  const pw=document.getElementById('pw').value.trim();
  try{{const h=await dec(pw);try{{sessionStorage.setItem('mls_pw',pw)}}catch(_){{}};show(h)}}
  catch(_){{e.textContent='Mật khẩu chưa đúng.';b.disabled=false;b.textContent='Xem tài liệu'}}
}});
(async()=>{{let pw=null;try{{pw=sessionStorage.getItem('mls_pw')}}catch(_){{}}
  if(pw&&window.crypto&&crypto.subtle){{try{{show(await dec(pw))}}catch(_){{}}}}}})();
</script></body></html>'''
open(out, 'w', encoding='utf-8').write(page)
print('ok', out, len(page))
