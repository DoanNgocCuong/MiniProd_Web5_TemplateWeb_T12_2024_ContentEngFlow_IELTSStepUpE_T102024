# Changelog

Note: Lần đầu viết Changlog.md (xài ChatGPT). Chi tiết xem ở DoanNgocCuong/home/Git....

## [1.2] - 2024-12-09
### Fixed
- Fixed bug: API không gen Audio (do lỗi CURL, chuyển sang `requests` library) cho:
  - `output_ipa`.
  - `output_meaning` (đọc câu hỏi).

### Added
- Thêm cột `week` trong dữ liệu:
  - Các đường link gen ra theo format:
    ```
    https://smedia.stepup.edu.vn/ielts/chunking/listening/week_<số tuần>/<số thứ tự>/ipa.mp3
    ```
  - Ví dụ:
    - [Week 1, File 999](https://smedia.stepup.edu.vn/ielts/chunking/listening/week_1/999/ipa.mp3)
    - [Week 25, File 2](https://smedia.stepup.edu.vn/ielts/chunking/listening/week_25/2/ipa.mp3)

### Notes for Next Version (1.3+)
1. **Check lỗi cột `answer 2 - feedback 2` trong `output_meaning`:**
   - Hiện tại không hiển thị đáp án.
   - Ghi chú: Phần cũ của anh Trúc có thể không có tính năng này (cần xác nhận thêm).
2. **Gen Ảnh:**
   - Tạm thời gen bằng AI (độ chính xác dự kiến 80%).
   - Kế hoạch bổ sung trong phiên bản tiếp theo.

---

