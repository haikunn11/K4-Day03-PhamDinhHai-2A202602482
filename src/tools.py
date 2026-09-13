"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Trợ lý Đơn hàng & Kho vận Chuỗi cung ứng (Supply Chain & Logistics Agent).
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu thông tin đơn hàng / kiện hàng trong kho
    {
        "name": "order_tracking",
        "description": "Tra cứu hồ sơ chi tiết, vị trí kệ kho lưu trữ, số lượng sản phẩm và trạng thái của đơn hàng trong chuỗi cung ứng bằng mã đơn hàng (order_id).",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng hoặc mã vận đơn cần tra cứu (ví dụ: 'ORD-2026-001')"
                }
            },
            "required": ["order_id"]
        }
    },
    
    # Tool 2 (TASK 1.2): Cập nhật trạng thái đơn hàng / tạo lệnh xuất kho
    {
        "name": "update_order_status",
        "description": "Cập nhật trạng thái đơn hàng (ví dụ: 'Đang xuất kho', 'Đang vận chuyển', 'Hoàn tất') và chỉ định vị trí kho/cửa xuất trong chuỗi cung ứng.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Mã đơn hàng cần cập nhật (ví dụ: 'ORD-2026-001')"
                },
                "new_status": {
                    "type": "string",
                    "description": "Trạng thái mới cần cập nhật cho đơn hàng (ví dụ: 'Đang xuất kho', 'Đang vận chuyển', 'Hoàn tất')"
                },
                "location": {
                    "type": "string",
                    "description": "Vị trí chuyển đến, cửa xuất kho hoặc bến bốc dỡ hàng (ví dụ: 'Cửa xuất số 02')"
                },
                "note": {
                    "type": "string",
                    "description": "Ghi chú điều phối bổ sung (nếu có)"
                }
            },
            "required": ["order_id", "new_status"]
        }
    },

    # Tool bổ trợ tương thích ngược cho bài toán học vụ mẫu (TODO 1.2)
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ hoặc buổi làm việc điều phối vận hành.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã định danh sinh viên hoặc nhân sự phụ trách (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn hoặc quản lý phụ trách (ví dụ: 'PGS.TS Nguyễn Văn A')"
                }
            },
            "required": ["student_id", "datetime_str"]
        }
    },

    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ sinh viên hoặc nhân sự phụ trách.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên hoặc mã nhân sự cần tra cứu"
                }
            },
            "required": ["student_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    # Dữ liệu Đơn hàng & Kho vận Chuỗi cung ứng (Manufacturing & Supply Chain)
    "ORD-2026-001": {
        "order_id": "ORD-2026-001",
        "customer": "Công ty Cổ phần Sản xuất VinFast",
        "item_name": "Bộ điều khiển trung tâm ECU & Cảm biến LiDAR",
        "quantity": 50,
        "warehouse_location": "Khu A - Kệ 04 - Tầng 2",
        "status": "Đã lưu kho sẵn sàng",
        "manager": "Kỹ sư Trần Đình Trọng",
        "notes": "Linh kiện kiểm định đạt chuẩn 100% ISO 9001"
    },
    "ORD-2026-002": {
        "order_id": "ORD-2026-002",
        "customer": "Nhà máy Sản xuất Pin Năng lượng VinES",
        "item_name": "Cell pin Lithium-ion 21700 cao cấp",
        "quantity": 2000,
        "warehouse_location": "Khu B - Kho mát tiêu chuẩn 20°C",
        "status": "Đã đóng gói hoàn tất",
        "manager": "Kỹ sư Lê Thu Hà",
        "notes": "Hàng dễ cháy nổ, yêu cầu xe tải chuyên dụng có điều hòa"
    },
    # Dữ liệu sinh viên mẫu để tương thích ngược
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}


def execute_order_tracking(order_id: str) -> str:
    """Thực thi tra cứu thông tin đơn hàng / kiện hàng chuỗi cung ứng"""
    clean_id = order_id.strip().upper()
    order = MOCK_DATABASE.get(clean_id)
    if order and "order_id" in order:
        return json.dumps({
            "status": "SUCCESS",
            "order_id": clean_id,
            "data": order
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu đơn hàng có mã '{order_id}' trong hệ thống kho vận."
        }, ensure_ascii=False)


def execute_update_order_status(order_id: str, new_status: str, location: str = "Cửa xuất số 01", note: str = "") -> str:
    """Thực thi cập nhật trạng thái đơn hàng hoặc tạo lệnh xuất kho"""
    clean_id = order_id.strip().upper()
    if clean_id in MOCK_DATABASE and "order_id" in MOCK_DATABASE[clean_id]:
        MOCK_DATABASE[clean_id]["status"] = new_status
        if location:
            MOCK_DATABASE[clean_id]["warehouse_location"] = location
        return json.dumps({
            "status": "SUCCESS",
            "dispatch_id": f"DISPATCH-{clean_id}-OK",
            "order_id": clean_id,
            "new_status": new_status,
            "location": location,
            "message": f"Đã cập nhật đơn hàng {clean_id}: Trạng thái '{new_status}', Điều chuyển tới '{location}'."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy đơn hàng '{order_id}' để cập nhật trạng thái."
        }, ensure_ascii=False)


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên (tương thích ngược)"""
    clean_id = student_id.strip().upper()
    student = MOCK_DATABASE.get(clean_id)
    if student and "full_name" in student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": clean_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn (tương thích ngược)"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "order_tracking": execute_order_tracking,
    "update_order_status": execute_update_order_status,
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
