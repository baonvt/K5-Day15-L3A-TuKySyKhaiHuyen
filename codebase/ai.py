"""Gọi OpenRouter hoặc chạy mô phỏng bằng quy tắc cho demo CP2.

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

Nối model thật: đặt MODEL_PROVIDER=openrouter, MODEL_NAME và API_KEY trong .env.
"""
import json
import os
import re
import urllib.error
import urllib.request
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
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MAX_TOKENS = 4096
REVIEW_SENTIMENTS = ("tich_cuc", "tieu_cuc", "lan_lon", "khong_ro")

# Dấu hiệu quyết định nhãn và nội dung giải thích hiển thị.
REVIEW_SIGNALS = {
    "trai_nghiem_cu_the": ("cao", "Review mô tả cụ thể về sản phẩm hoặc trải nghiệm sử dụng"),
    "thieu_chi_tiet": ("chua_ro", "Review có quá ít chi tiết để đánh giá độ tin cậy"),
    "tin_hieu_lan_lon": ("chua_ro", "Review có dấu hiệu lẫn lộn nên chưa đủ căn cứ để đánh giá"),
    "khen_chung_chung": ("thap", "Review chỉ khen chung chung và thiếu chi tiết về sản phẩm"),
    "san_pham_khac": ("thap", "Review nói về sản phẩm khác với sản phẩm đang được phân tích"),
    "trung_lap": ("thap", "Câu chữ gần như trùng với một review khác trong cùng bộ"),
    "quang_cao": ("thap", "Review có lời kêu gọi mua hoặc thông tin quảng cáo"),
    "sao_lech_noi_dung": ("thap", "Điểm {stars} sao lệch rõ với nội dung đánh giá"),
    "chi_dan_he_thong": ("thap", "Review chứa chỉ dẫn yêu cầu hệ thống thay đổi cách xử lý"),
}

SUMMARY_ITEM = {
    "type": "object",
    "properties": {
        "noi_dung": {"type": "string"},
        "nguon": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["noi_dung", "nguon"],
    "additionalProperties": False,
}
REVIEW_ITEM = {
    "type": "object",
    "properties": {
        "sac_thai": {"type": "string", "enum": list(REVIEW_SENTIMENTS)},
        "dau_hieu": {"type": "string", "enum": list(REVIEW_SIGNALS)},
        "trich_dan": {"type": "string"},
    },
    "required": ["sac_thai", "dau_hieu", "trich_dan"],
    "additionalProperties": False,
}


def _analysis_schema(payload):
    review_ids = [review["ma"] for review in payload["reviews"]]
    decisions = ["phan_tich"]
    if payload["loi_nguoi_dung"]:
        decisions.append("tu_choi")
    return {
        "type": "object",
        "properties": {
            "quyet_dinh": {"type": "string", "enum": decisions},
            "nhan": {
                "type": "object",
                "properties": dict.fromkeys(review_ids, REVIEW_ITEM),
                "required": review_ids,
                "additionalProperties": False,
            },
            "uu_diem": {"type": "array", "items": SUMMARY_ITEM},
            "nhuoc_diem": {"type": "array", "items": SUMMARY_ITEM},
        },
        "required": ["quyet_dinh", "nhan", "uu_diem", "nhuoc_diem"],
        "additionalProperties": False,
    }


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


def _mock_signal(review, product_type, duplicate, positive, negative):
    content = review["noi_dung"]
    if command := REVIEW_COMMAND.search(content):
        return "chi_dan_he_thong", command.group()
    if promotion := PROMOTION.search(content):
        return "quang_cao", promotion.group()
    if duplicate:
        return "trung_lap", content
    other_type = PRODUCT_TYPES.match(content.casefold())
    if product_type and other_type and other_type.group() != product_type.group():
        return "san_pham_khac", other_type.group()
    if review["sao"] == 5 and negative and not positive:
        return "sao_lech_noi_dung", negative[0]
    if review["sao"] == 1 and positive and not negative:
        return "sao_lech_noi_dung", positive[0]
    feature = FEATURE.search(content)
    praise = GENERIC_PRAISE.search(content)
    if not feature and praise:
        return "khen_chung_chung", praise.group()
    if feature and len(content.split()) >= 4:
        return "trai_nghiem_cu_the", (positive + negative or [feature.group()])[0]
    return "thieu_chi_tiet", content


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
    result = {"quyet_dinh": "phan_tich", "nhan": {}, "uu_diem": [], "nhuoc_diem": []}
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
        signal, excerpt = _mock_signal(review, product_type, duplicate, positive, negative)
        if positive and negative:
            sentiment = "lan_lon"
        elif negative:
            sentiment = "tieu_cuc"
        elif positive or signal == "khen_chung_chung":
            sentiment = "tich_cuc"
        else:
            sentiment = "khong_ro"
        result["nhan"][review_id] = {"sac_thai": sentiment, "dau_hieu": signal, "trich_dan": excerpt}
        if REVIEW_SIGNALS[signal][0] != "thap":
            for key, clauses in (("uu_diem", positive), ("nhuoc_diem", negative)):
                result[key].extend({"noi_dung": clause, "nguon": [review_id]} for clause in clauses[:2])
    return result


def _call_openrouter(system: str, user: str) -> dict:
    if not MODEL_NAME or not API_KEY:
        raise ValueError("OpenRouter cần MODEL_NAME và API_KEY trong .env.")

    payload = json.loads(user)
    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "phan_tich_review", "strict": True, "schema": _analysis_schema(payload),
            },
        },
        "provider": {"require_parameters": True},
        "max_tokens": min(OPENROUTER_MAX_TOKENS, 512 + 110 * len(payload["reviews"])),
        "temperature": 0,
    }
    request = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 402:
            raise RuntimeError(
                "OpenRouter trả về HTTP 402. Hãy kiểm tra số dư và hạn mức của API key."
            ) from None
        raise RuntimeError(f"OpenRouter trả về HTTP {error.code}.") from None

    if data.get("error"):
        raise RuntimeError("OpenRouter báo lỗi khi tạo phản hồi.")
    choices = data.get("choices") or []
    if not choices or choices[0].get("error"):
        raise RuntimeError("OpenRouter không trả về lựa chọn hợp lệ.")
    content = choices[0]["message"].get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenRouter trả về nội dung rỗng.")

    usage = data.get("usage") or {}
    tokens_in = usage.get("prompt_tokens")
    tokens_out = usage.get("completion_tokens")
    if not isinstance(tokens_in, int) or not isinstance(tokens_out, int):
        raise RuntimeError("Phản hồi OpenRouter thiếu số token trong usage.")
    return {
        "text": content,
        "model": data.get("model") or MODEL_NAME,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
    }


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

    if MODEL_PROVIDER == "openrouter":
        return _call_openrouter(system, user)

    raise NotImplementedError(
        "MODEL_PROVIDER hiện hỗ trợ openrouter và fake."
    )
