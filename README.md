# Mai Linh Social – Taxi Social Web3

Trang tổng quan & khái toán sơ bộ dự án **Hệ sinh thái Mạng xã hội Taxi Web3** gửi anh John Davis.

- Trang web: `public/index.html` (một file duy nhất, ảnh và file Excel đã nhúng sẵn)
- Tài liệu: `docs/` – khái toán sơ bộ (Excel), tài liệu yêu cầu (Word)
- Mật khẩu trang: gửi riêng cho khách, không ghi trong repo
- Địa chỉ dự kiến: https://taxisocial.bbl.id.vn

## Deploy lên VPS (Nginx)

1. DNS của `bbl.id.vn`: thêm bản ghi `A  taxisocial  <IP VPS>`
2. Trên VPS:
   ```bash
   git clone <url-repo> taxi-social-web3 && cd taxi-social-web3
   sudo bash deploy/deploy.sh
   ```
3. Cập nhật lần sau: `git pull && sudo bash deploy/deploy.sh`

Yêu cầu trên VPS: `nginx`, `certbot` + `python3-certbot-nginx`.

> Lưu ý: mật khẩu trên trang chỉ chặn ở phía trình duyệt. Repo để **private**; chỉ đưa tài liệu bản gửi khách vào repo.
