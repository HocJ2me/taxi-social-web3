# Mai Linh Social – Taxi Social Web3

Trang tổng quan & khái toán sơ bộ dự án **Hệ sinh thái Mạng xã hội Taxi Web3** gửi anh John Davis.

- Trang web: `public/index.html` (một file duy nhất, ảnh và file Excel đã nhúng sẵn)
- Tài liệu: `docs/` – khái toán sơ bộ (Excel), tài liệu yêu cầu (Word)
- Mật khẩu trang: gửi riêng cho khách, không ghi trong repo
- GitHub Pages: https://hocj2me.github.io/taxi-social-web3/
- Tên miền riêng (tùy chọn): https://taxisocial.bbl.id.vn

## Bảo mật trang

`public/index.html` được **mã hóa AES-256-GCM** bằng mật khẩu (khóa sinh bằng PBKDF2-SHA256, 300.000 vòng). Ai không có mật khẩu chỉ thấy màn hình nhập mật khẩu, kể cả khi xem mã nguồn.

Cập nhật nội dung trang:
```bash
python3 -m pip install cryptography
python3 tools/encrypt_page.py trang_goc.plain.html '<mật khẩu>' public/index.html
git add public/index.html && git commit -m "Cập nhật trang" && git push
```
Trang gốc chưa mã hóa đặt tên `*.plain.html` để `.gitignore` chặn, không commit.

## GitHub Pages

Workflow `.github/workflows/pages.yml` tự xuất bản thư mục `public/` mỗi lần push vào `main` (thư mục `docs/` không được xuất bản).
Bật một lần: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Deploy lên VPS (Nginx) – tùy chọn

1. DNS của `bbl.id.vn`: thêm bản ghi `A  taxisocial  <IP VPS>`
2. Trên VPS:
   ```bash
   git clone <url-repo> taxi-social-web3 && cd taxi-social-web3
   sudo bash deploy/deploy.sh
   ```
3. Cập nhật lần sau: `git pull && sudo bash deploy/deploy.sh`

Yêu cầu trên VPS: `nginx`, `certbot` + `python3-certbot-nginx`.

> Lưu ý: mật khẩu trên trang chỉ chặn ở phía trình duyệt. Repo để **private**; chỉ đưa tài liệu bản gửi khách vào repo.
