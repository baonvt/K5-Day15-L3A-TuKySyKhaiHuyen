"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    phân tích bằng quy tắc minh họa, model "fake", token 0 — để chạy hết luồng CP2.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import re
from difflib import SequenceMatcher

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


OUT_OF_SCOPE = re.compile(
    r"bỏ qua.{0,40}(?:hướng dẫn|quy tắc|chỉ dẫn)|"
    r"(?:tiết lộ|in ra|cho xem).{0,40}(?:prompt|api key|hướng dẫn hệ thống)|"
    r"(?:viết|tạo|soạn|đăng|sinh)\s+(?:cho tôi\s+)?(?:một\s+|vài\s+|\d+\s+)?"
    r"(?:review|đánh giá|bình luận)|"
    r"lừa đảo|(?:chắc chắn|khẳng định|xác nhận).{0,50}(?:giả|thật)|"
    r"(?:nên mua|đừng mua|có nên mua|mua hay không)",
    re.IGNORECASE,
)
REVIEW_REQUEST = re.compile(
    r"review|đánh giá|tin cậy|đáng tin|điểm sao|ưu.{0,8}nhược|phân tích|tóm tắt",
    re.IGNORECASE,
)
REVIEW_COMMAND = re.compile(
    r"bỏ qua.{0,40}(?:hướng dẫn|chỉ dẫn|quy tắc)|"
    r"(?:gắn nhãn|đánh dấu).{0,35}(?:tất cả|mọi review|toàn bộ)|"
    r"(?:tiết lộ|in ra).{0,35}(?:prompt|hướng dẫn hệ thống)",
    re.IGNORECASE,
)
PROMOTION = re.compile(
    r"https?://|\bwww\.|mã giảm|voucher|inbox|(?:mua|đặt hàng) ngay|"
    r"mua liền|\b(?:0|\+84)(?:[ .-]?\d){9}\b",
    re.IGNORECASE,
)
GENERIC_PRAISE = re.compile(
    r"tuyệt vời|shop uy tín|10 điểm|hài lòng|xuất sắc|tốt lắm|"
    r"chất lượng tốt|rất tốt|đóng gói đẹp|giao hàng nhanh",
    re.IGNORECASE,
)
FEATURE = re.compile(
    r"\b(?:pin|bass|âm thanh|âm lượng|sạc|màn hình|camera|wifi|"
    r"kết nối|tai trái|tai phải|bàn phím|cổng|mic|micro|"
    r"độ trễ|chống ồn|cảm ứng|đeo|tốc độ|nhiệt độ|dung lượng|loa)\b",
    re.IGNORECASE,
)
POSITIVE = re.compile(
    r"(?:không đau|không nóng|không bị rè|dùng được|\b(?:tốt|"
    r"bền|nhanh|rõ|êm|thoải mái|mượt|ổn|nhạy|lâu)\b)",
    re.IGNORECASE,
)
NEGATIVE = re.compile(
    r"mất tiếng|hết pin|khó kết nối|không (?:sạc|kết nối|hoạt động|lên nguồn)|"
    r"\b(?:yếu|rè|chậm|lỏng|lag|hỏng|lỗi|đơ|đau|nóng|kém|tụt)\b",
    re.IGNORECASE,
)
NEGATED_PROBLEMS = re.compile(r"không\s+(?:bị\s+)?(?:đau|nóng|rè|lỗi|lag)", re.IGNORECASE)
PRODUCT_TYPES = re.compile(
    r"\b(?:tai nghe|sạc điện thoại|điện thoại|laptop|chuột|bàn phím|củ sạc|loa)\b"
)


def _mock_label(review, product_type, duplicate, positive, negative):
    content = review["noi_dung"]
    if REVIEW_COMMAND.search(content):
        return "thap", "Review chứa chỉ dẫn yêu cầu hệ thống thay đổi cách xử lý."
    if PROMOTION.search(content):
        return "thap", "Review có lời kêu gọi mua hoặc thông tin quảng cáo."
    if duplicate:
        return "thap", f"Câu chữ gần như trùng với review {duplicate} trong cùng bộ."
    other_type = PRODUCT_TYPES.match(content.casefold())
    if product_type and other_type and other_type.group() != product_type.group():
        return "thap", f"Review mở đầu bằng nhóm sản phẩm khác: {other_type.group()}."
    if (review["sao"] == 5 and negative and not positive) or (
        review["sao"] == 1 and positive and not negative
    ):
        return "thap", "Số sao lệch hẳn với nội dung đánh giá."
    feature = FEATURE.search(content)
    if not feature and GENERIC_PRAISE.search(content):
        return "thap", "Review chỉ khen chung chung và thiếu chi tiết về sản phẩm."
    if feature and len(content.split()) >= 4:
        return "cao", f"Review mô tả chi tiết liên quan đến {feature.group().lower()}."
    return "chua_ro", "Review có quá ít chi tiết về trải nghiệm sử dụng."


def _mock_analysis(payload):
    request = payload["loi_nguoi_dung"]
    if request and OUT_OF_SCOPE.search(request):
        return {"quyet_dinh": "tu_choi"}
    if request and not (
        REVIEW_REQUEST.search(request) or request.startswith(("Sản phẩm:", "["))
    ):
        return {"quyet_dinh": "tu_choi"}

    reviews = payload["reviews"]
    product_type = PRODUCT_TYPES.search(payload["san_pham"].casefold())
    normalized = [" ".join(re.findall(r"\w+", review["noi_dung"].casefold())) for review in reviews]
    result = {"quyet_dinh": "phan_tich", "nhan": [], "uu_diem": [], "nhuoc_diem": []}
    for index, review in enumerate(reviews):
        review_id = review["ma"]
        content = review["noi_dung"]
        duplicate = next((
            other["ma"]
            for other_index, other in enumerate(reviews)
            if other_index != index
            and len(normalized[index]) >= 20
            and SequenceMatcher(None, normalized[index], normalized[other_index]).ratio() >= 0.9
        ), None)
        positive = []
        negative = []
        for clause in re.split(r"[,;.!?\n]+", content):
            clause = clause.strip()
            if NEGATIVE.search(NEGATED_PROBLEMS.sub("", clause)):
                negative.append(clause)
            elif POSITIVE.search(clause):
                positive.append(clause)
        label, reason = _mock_label(review, product_type, duplicate, positive, negative)
        result["nhan"].append({"ma": review_id, "nhan": label, "ly_do": reason})
        if label != "thap":
            for key, clauses in (("uu_diem", positive), ("nhuoc_diem", negative)):
                result[key].extend({"noi_dung": clause, "nguon": [review_id]} for clause in clauses[:2])
    return result


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        analysis = _mock_analysis(json.loads(user))
        return {
            "text": json.dumps(analysis, ensure_ascii=False),
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }

    # NHÓM VIẾT: gọi model thật ở đây (theo MODEL_PROVIDER, MODEL_NAME, API_KEY) rồi trả đúng 4 khoá.
    # Ví dụ chép được cho từng nhà cung cấp: docs/connect-model.md mục 2.
    raise NotImplementedError(
        "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
        % MODEL_PROVIDER)
