# -*- coding: utf-8 -*-
"""湊 24 對戰——題庫產生器（規格 §8.1，build 期執行）。

窮舉 1–10 取 4（可重複）的多重集合，對每組窮舉所有合併順序與運算符，
套用 D-1 過濾（中間結果為非負整數、除法必須整除），以合併樹正規化形式去重。
輸出符合規格 §7 Deal 型別的清單；canonicalSolution 優先選第一步為乘法或加法者。
"""

from itertools import combinations_with_replacement

TARGET = 24


def _canon(tree):
    """合併樹正規化：加法與乘法子樹排序（交換律），用於解法去重。"""
    if not isinstance(tree, tuple):
        return str(tree)
    op, l, r = tree
    cl, cr = _canon(l), _canon(r)
    if op in "+*" and cl > cr:
        cl, cr = cr, cl
    return f"({cl}{op}{cr})"


def solve(values):
    """回傳 {正規化樹: steps}；steps 為 [(left, op, right, result)] 三步（數值序列）。"""
    results = {}

    def rec(items, steps):
        if len(items) == 1:
            if items[0][0] == TARGET:
                key = _canon(items[0][1])
                if key not in results:
                    results[key] = list(steps)
            return
        n = len(items)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                a, ta = items[i]
                b, tb = items[j]
                rest = [items[k] for k in range(n) if k not in (i, j)]
                for op in "+-*/":
                    if op in "+*" and i > j:
                        continue  # 交換律剪枝
                    if op == "+":
                        v = a + b
                    elif op == "*":
                        v = a * b
                    elif op == "-":
                        v = a - b
                        if v < 0:  # D-1：非負
                            continue
                    else:
                        if b == 0 or a % b != 0:  # D-1：整除
                            continue
                        v = a // b
                    rec(rest + [(v, (op, ta, tb))],
                        steps + [(a, op, b, v)])

    rec([(v, v) for v in values], [])
    return results


def _pick_canonical(solutions):
    """優先選第一步為 × 或 ＋ 的解（演示較易理解）。"""
    ranked = sorted(
        solutions.values(),
        key=lambda steps: (0 if steps[0][1] in "*+" else 1, steps))
    return ranked[0]


def build_deals():
    """產生全部有解牌組，回傳規格 §7 Deal dict 清單。"""
    deals = []
    for combo in combinations_with_replacement(range(1, 11), 4):
        sols = solve(list(combo))
        if not sols:
            continue
        count = len(sols)
        canonical = _pick_canonical(sols)
        only = list(sols.values())
        has_div_only = count <= 2 and any(
            any(s[1] == "/" for s in steps) for steps in only)
        if count >= 8:
            diff = "easy"
        elif count >= 3:
            diff = "medium"
        else:
            diff = "hard"
        if has_div_only:
            diff = "hard"
        deals.append({
            "id": "-".join(str(v) for v in combo),
            "values": list(combo),
            "solutionCount": count,
            "difficulty": diff,
            "canonicalSolution": [
                {"left": s[0], "op": s[1], "right": s[2], "result": s[3]}
                for s in canonical],
        })
    return deals


def verify(deals):
    """AC-15：每筆 canonicalSolution 重現且結果為 24、solutionCount ≥ 1。"""
    for d in deals:
        assert d["solutionCount"] >= 1, d["id"]
        pool = list(d["values"])
        for s in d["canonicalSolution"]:
            assert s["left"] in pool, d["id"]
            pool.remove(s["left"])
            assert s["right"] in pool, d["id"]
            pool.remove(s["right"])
            l, r = s["left"], s["right"]
            v = {"+": l + r, "-": l - r, "*": l * r,
                 "/": (l // r if r and l % r == 0 else None)}[s["op"]]
            assert v == s["result"] and v is not None and v >= 0, d["id"]
            pool.append(v)
        assert pool == [24], d["id"]
    return True


if __name__ == "__main__":
    ds = build_deals()
    verify(ds)
    from collections import Counter
    c = Counter(d["difficulty"] for d in ds)
    print(f"deals: {len(ds)} / 715  |  easy {c['easy']}  medium {c['medium']}  hard {c['hard']}")
