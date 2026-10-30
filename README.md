# Mai Linh Social – Taxi Social Web3

Trang tổng quan & khái toán sơ bộ dự án **Hệ sinh thái Mạng xã hội Taxi Web3** gửi anh John Davis.

Địa chỉ: **https://hocj2me.github.io/taxi-social-web3/**

## Bật GitHub Pages (một lần)

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: `main`, thư mục `/ (root)` → Save.

## Bảo mật

`index.html` được mã hóa AES-256-GCM bằng mật khẩu (PBKDF2-SHA256, 300.000 vòng). Không có mật khẩu chỉ thấy màn hình nhập mật khẩu, kể cả khi xem mã nguồn. Mật khẩu gửi riêng cho khách, không ghi trong repo.

## Cập nhật trang

```bash
python3 -m pip install cryptography
python3 tools/encrypt_page.py trang_goc.plain.html '<mật khẩu>' index.html
git add index.html && git commit -m "Cập nhật trang" && git push
```
Trang gốc chưa mã hóa đặt tên `*.plain.html` (bị `.gitignore` chặn), không commit.
