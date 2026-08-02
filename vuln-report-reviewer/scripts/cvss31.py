#!/usr/bin/env python3
"""CVSS 3.1 基础分值计算器 + 报告自洽性核验。

用途：漏洞提交报告审核时，强制核验"向量 → 分值 → 文字定级"三者一致。
报告中任何 CVSS 声称值都必须经本脚本复核，禁止心算。

用法：
  python3 cvss31.py "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N"
  python3 cvss31.py "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N" --claimed 7.5 --claimed-label 高危

退出码：0 = 计算成功（若给 --claimed 则一致）；1 = 参数错误；2 = 声称值不一致。
"""
import argparse
import math
import re
import sys

METRICS = {
    "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20},
    "AC": {"L": 0.77, "H": 0.44},
    "UI": {"N": 0.85, "R": 0.62},
    "CIA": {"N": 0.0, "L": 0.22, "H": 0.56},
}
REQUIRED = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
BANDS = [(0.0, "None/无"), (0.1, "Low/低危"), (4.0, "Medium/中危"), (7.0, "High/高危"), (9.0, "Critical/严重")]
BAND_LABELS = {"None/无": 0.0, "Low/低危": 0.1, "Medium/中危": 4.0, "High/高危": 7.0, "Critical/严重": 9.0}
ZH_LABEL = {"无": "None/无", "低危": "Low/低危", "中危": "Medium/中危", "高危": "High/高危", "严重": "Critical/严重"}


def roundup(x: float) -> float:
    i = round(x * 100000)
    return (i // 10000 + (1 if i % 10000 else 0)) / 10.0


def pr_value(pr: str, scope: str) -> float:
    table = {"N": 0.85, "L": 0.62 if scope == "U" else 0.68, "H": 0.27 if scope == "U" else 0.50}
    if pr not in table:
        raise ValueError(f"PR 非法值: {pr}")
    return table[pr]


def band(score: float) -> str:
    label = BANDS[0][1]
    for threshold, name in BANDS:
        if score >= threshold:
            label = name
    return label


def parse_vector(vector: str) -> dict:
    v = vector.strip()
    v = re.sub(r"^CVSS:3\.[01]/", "", v, flags=re.IGNORECASE)
    parts = {}
    for item in v.split("/"):
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"无法解析的分段: {item!r}")
        k, val = item.split(":", 1)
        parts[k.strip().upper()] = val.strip().upper()
    missing = [m for m in REQUIRED if m not in parts]
    if missing:
        raise ValueError(f"缺少必需指标: {', '.join(missing)}")
    return parts


def compute(m: dict) -> float:
    scope = m["S"]
    if scope not in ("U", "C"):
        raise ValueError(f"S 非法值: {scope}")
    av = METRICS["AV"][m["AV"]]
    ac = METRICS["AC"][m["AC"]]
    ui = METRICS["UI"][m["UI"]]
    c = METRICS["CIA"][m["C"]]
    i = METRICS["CIA"][m["I"]]
    a = METRICS["CIA"][m["A"]]
    pr = pr_value(m["PR"], scope)

    isc = 1 - (1 - c) * (1 - i) * (1 - a)
    if scope == "U":
        impact = 6.42 * isc
    else:
        impact = 7.52 * (isc - 0.029) - 3.25 * (isc - 0.02) ** 15
    exploitability = 8.22 * av * ac * pr * ui
    if impact <= 0:
        return 0.0
    base = impact + exploitability if scope == "U" else 1.08 * (impact + exploitability)
    return roundup(min(base, 10.0))


def main() -> int:
    ap = argparse.ArgumentParser(description="CVSS 3.1 分值计算与报告自洽核验")
    ap.add_argument("vector", help="CVSS 向量，可带或不带 CVSS:3.1/ 前缀")
    ap.add_argument("--claimed", type=float, default=None, help="报告中声称的分值")
    ap.add_argument("--claimed-label", default=None, help="报告中声称的文字定级（低危/中危/高危/严重）")
    args = ap.parse_args()

    try:
        metrics = parse_vector(args.vector)
        score = compute(metrics)
    except (ValueError, KeyError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    severity = band(score)
    print(f"向量:   {args.vector}")
    print(f"分值:   {score}")
    print(f"等级:   {severity}")

    ok = True
    if args.claimed is not None:
        if abs(args.claimed - score) < 1e-9:
            print(f"[PASS] 声称分值 {args.claimed} 与计算值一致")
        else:
            print(f"[FAIL] 声称分值 {args.claimed} ≠ 计算值 {score} —— 报告须改其一")
            ok = False
    if args.claimed_label is not None:
        want = ZH_LABEL.get(args.claimed_label.strip())
        if want is None:
            print(f"[WARN] 无法识别文字定级: {args.claimed_label}")
        elif want == severity:
            print(f"[PASS] 文字定级「{args.claimed_label}」落在 {severity} 区间")
        else:
            print(f"[FAIL] 文字定级「{args.claimed_label}」与分值区间 {severity} 不符 —— 报告须改其一")
            ok = False
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
