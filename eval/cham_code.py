"""Chấm tự động 2 metric `code` trong eval/metric_spec.yaml cho một lượt eval/run-N.csv.

    python eval/cham_code.py eval/run-1.csv

- M1 dung_dinh_dang_va_diem_sao: đúng định dạng docs/answer-format.md, sao gốc khớp pass_criterion,
  sao tính lại khớp công thức áp trên chính nhãn output đã gắn (sai lệch ≤ 0.05).
- M2 nhan_khop_du_lieu (chỉ câu có review): (a) không review spam nào bị gắn Độ tin cậy cao,
  (b) không review không spam nào bị gắn Độ tin cậy thấp, (c) có ít nhất một review spam bị gắn Độ tin cậy thấp.
  Tập review spam lấy từ pass_criterion ("review spam = {R2, R5}").
Kèm cột "yêu cầu riêng": các điều thêm trong pass_criterion kiểm được bằng code (LƯU Ý nêu quá ít review / thiếu sao).
M3, M4 (grader nguoi) KHÔNG chấm ở đây. Script chỉ in kết quả, không sửa file lượt.
"""
import csv
import re
import sys

LABELS = {"Độ tin cậy cao", "Chưa rõ độ tin cậy", "Độ tin cậy thấp"}
HIGH, LOW = "Độ tin cậy cao", "Độ tin cậy thấp"
SECTIONS = ["NHÃN TỪNG REVIEW:", "ƯU ĐIỂM:", "NHƯỢC ĐIỂM:"]
REVIEW = re.compile(r"^\[([1-5?])\]\s*(.*)$", re.DOTALL)
LABEL_LINE = re.compile(r"^R(\d+) \| (.*?) \| (.*)$")
TOL = 0.05 + 1e-9


def reviews_of(text):
    if "||" not in text:
        return []
    out = []
    for part in text.split("||"):
        m = REVIEW.fullmatch(part.strip())
        if m and len(out) < 30:
            out.append(None if m.group(1) == "?" else int(m.group(1)))
    return out


def number(pattern, line):
    m = re.search(pattern, line)
    return float(m.group(1)) if m else None


def grade(row):
    out = (row.get("output") or "").replace("\r\n", "\n").strip()
    stars = reviews_of(row["input"])
    n = len(stars)
    crit = row.get("pass_criterion", "")
    kind = "KHÔNG XỬ LÝ:" if row["type"] == "tu_choi" else ("SẢN PHẨM:" if n else "CẦN THÊM THÔNG TIN:")
    if (row.get("error") or "").strip() or not out:
        why = "không có output (lỗi: %s)" % (row.get("error") or "output rỗng").strip()
        return "K", ("K" if n else "—"), "—", why
    lines = [l.strip() for l in out.split("\n") if l.strip()]
    notes = []
    if not lines[0].startswith(kind):
        notes.append("dòng đầu không phải %s" % kind)
    if not n:
        return ("K" if notes else "Đ"), "—", "—", "; ".join(notes)

    # ---- M1 với câu có review
    for s in SECTIONS:
        if s not in lines:
            notes.append("thiếu mục %s" % s)
    star_line = next((l for l in lines if l.startswith("ĐIỂM SAO:")), None)
    note_line = next((l for l in lines if l.startswith("LƯU Ý:")), None)
    if not star_line:
        notes.append("thiếu dòng ĐIỂM SAO")
    if not note_line:
        notes.append("thiếu dòng LƯU Ý")
    labels = {}
    for l in lines:
        m = LABEL_LINE.match(l)
        if m:
            labels["R" + m.group(1)] = m.group(2).strip()
    want_ids = ["R%d" % i for i in range(1, n + 1)]
    if list(labels) != want_ids:
        notes.append("dòng nhãn %s, cần %s" % (",".join(labels) or "không có", ",".join(want_ids)))
    bad = [k for k, v in labels.items() if v not in LABELS]
    if bad:
        notes.append("nhãn lạ ở %s" % ",".join(bad))
    if star_line:
        exp_goc = number(r"sao gốc (\d+(?:\.\d+)?)", crit)
        goc = number(r"gốc (\d+(?:\.\d+)?)", star_line)
        if exp_goc is not None and (goc is None or abs(goc - exp_goc) > TOL):
            notes.append("sao gốc %s, cần %.2f" % (goc, exp_goc))
        kept = [s for rid, s in zip(want_ids, stars) if labels.get(rid) != LOW and s is not None]
        lai = number(r"tính lại (\d+(?:\.\d+)?)", star_line)
        if kept:
            exp_lai = sum(kept) / len(kept)
            if lai is None or abs(lai - exp_lai) > TOL:
                notes.append("sao tính lại %s, theo nhãn đã gắn phải là %.2f" % (lai, exp_lai))
        elif "không tính được" not in star_line.split("tính lại", 1)[-1]:
            notes.append("không còn review giữ có sao nhưng không ghi 'không tính được'")
    m1 = "K" if notes else "Đ"

    # ---- M2
    spam = set(re.findall(r"R\d+", (re.search(r"review spam = \{([^}]*)\}", crit) or [None, ""])[1]))
    m2_notes = []
    hi = sorted(r for r in spam if labels.get(r) == HIGH)
    lo = sorted(r for r in labels if r not in spam and labels[r] == LOW)
    if hi:
        m2_notes.append("spam gắn cao: %s" % ",".join(hi))
    if lo:
        m2_notes.append("review thật gắn thấp: %s" % ",".join(lo))
    if spam and not any(labels.get(r) == LOW for r in spam):
        m2_notes.append("không spam nào gắn thấp")
    m2 = "K" if m2_notes else "Đ"

    # ---- yêu cầu riêng trong pass_criterion
    extra = []
    if "quá ít review" in crit and not (note_line and "ít review" in note_line):
        extra.append("LƯU Ý chưa nêu quá ít review")
    if "không rõ số sao" in crit and not (note_line and ("thiếu số sao" in note_line or "không rõ số sao" in note_line)):
        extra.append("LƯU Ý chưa nêu review thiếu sao")
    ex = "K" if extra else "Đ"
    return m1, m2, ex, "; ".join(notes + m2_notes + extra)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    with open(sys.argv[1], encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    print("| Câu | type | M1 | M2 | Yêu cầu riêng | Ghi chú |")
    print("|---|---|---|---|---|---|")
    tally = {"M1": [0, 0], "M2": [0, 0]}
    for r in rows:
        m1, m2, ex, why = grade(r)
        print("| %s | %s | %s | %s | %s | %s |" % (r["id"], r["type"], m1, m2, ex, why))
        for k, v in (("M1", m1), ("M2", m2)):
            if v != "—":
                tally[k][1] += 1
                tally[k][0] += v == "Đ"
    for k, (a, b) in tally.items():
        print("%s: %d/%d đạt (%.0f%%)" % (k, a, b, 100.0 * a / b if b else 0))


if __name__ == "__main__":
    main()
