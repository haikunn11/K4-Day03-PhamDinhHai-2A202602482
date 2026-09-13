# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Phạm Đình Hải  
> **Mã Sinh Viên / Mã Học viên:** 2A202602482  
> **Chủ đề Lựa chọn:** Gợi ý 3.2: Trợ lý Đơn hàng & Kho vận Chuỗi cung ứng (Supply Chain & Logistics Agent)  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Quy trình kho vận đòi hỏi chuỗi suy luận liên hoàn: nhận diện mã vận đơn/kiện hàng -> tra cứu vị trí kho và tình trạng sẵn sàng -> ra quyết định điều chuyển hoặc xuất kho. |
| **2. Tool Interaction** | 5 / 5 | Hệ thống bắt buộc phải tương tác thời gian thực với hệ thống WMS/ERP thông qua MCP Server để truy vấn dữ liệu tồn kho thực tế và cập nhật trạng thái đơn hàng, không thể dựa vào tri thức tĩnh của LLM. |
| **3. Dynamic Decision** | 5 / 5 | Hành động tiếp theo phụ thuộc hoàn toàn vào kết quả quan sát (Observation): nếu đơn hàng đang ở trạng thái 'Đã lưu kho sẵn sàng' thì mới cho phép tạo lệnh xuất kho; nếu 'Chưa đóng gói' hoặc 'Không tìm thấy' thì phản hồi cảnh báo thích hợp. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải duy trì ngữ cảnh và bám sát mục tiêu điều phối đơn hàng từ khâu tiếp nhận yêu cầu, định vị lưu kho, đến xác nhận trạng thái bàn giao vận chuyển. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Tổng điểm 18/20 (> 12/20): Bài toán nghiệp vụ Chuỗi cung ứng & Kho vận cực kỳ phù hợp để phát triển bằng kiến trúc Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật (`gemini-3.6-flash` kết nối `vinuni-academic-mcp-server`):

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin chi tiết và vị trí lưu kho của đơn hàng ORD-2026-001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "order_tracking",
    "arguments": {
      "order_id": "ORD-2026-001"
    },
    "observation": {
      "status": "SUCCESS",
      "order_id": "ORD-2026-001",
      "data": {
        "order_id": "ORD-2026-001",
        "customer": "Công ty Cổ phần Sản xuất VinFast",
        "item_name": "Bộ điều khiển trung tâm ECU & Cảm biến LiDAR",
        "quantity": 50,
        "warehouse_location": "Khu A - Kệ 04 - Tầng 2",
        "status": "Đã lưu kho sẵn sàng",
        "manager": "Kỹ sư Trần Đình Trọng",
        "notes": "Linh kiện kiểm định đạt chuẩn 100% ISO 9001"
      }
    },
    "latency_ms": 2842.28
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin chi tiết và vị trí lưu kho của đơn hàng ORD-2026-001.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Kết quả tra cứu đơn hàng ORD-2026-001 (Bộ điều khiển trung tâm ECU & Cảm biến LiDAR): Khách hàng: Công ty Cổ phần Sản xuất VinFast, Số lượng: 50, Vị trí lưu kho: Khu A - Kệ 04 - Tầng 2, Trạng thái: Đã lưu kho sẵn sàng, Người phụ trách: Kỹ sư Trần Đình Trọng, Ghi chú: Linh kiện kiểm định đạt chuẩn 100% ISO 9001.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini: `gemini-3.6-flash`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (`order_tracking` cho TC02, TC04, TC05; `update_order_status` cho TC03; TC01 trả lời trực tiếp không cần Tool).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
