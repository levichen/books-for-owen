# -*- coding: utf-8 -*-
"""聰明餅乾（Smart Cookies）題目生成器。

仿 FoxMind 的單人邏輯遊戲：9 片餅乾（三角／正方／圓 × 紅／黃／藍）放進 3×3 烤盤，
依圖像線索推理出唯一擺法。64 題分 8 級，每級逐步引入新線索類型。

餅乾編號 k = shape*3 + color（shape: 0 三角 1 正方 2 圓；color: 0 紅 1 黃 2 藍）。
格子編號 cell = row*3 + col。

線索類型（t）：
  at   餅乾 k 在格子 cell            sat  格子 cell 是某形狀 s      cat  格子 cell 是某顏色 c
  nat  餅乾 k 不在格子 cell          rel  餅乾 a 緊鄰餅乾 b（d='L' a 在 b 左邊；d='U' a 在 b 上面）
  row  餅乾 k 在第 i 列              col  餅乾 k 在第 i 行
  nrow 餅乾 k 不在第 i 列            ncol 餅乾 k 不在第 i 行

題目以固定種子生成後存成 smart_cookies_puzzles.json（存在即沿用），
避免改生成器就讓孩子的過關紀錄對不上題目。重生：刪 json 後執行本檔。
"""

import json
import os
import random

SEED = 20261022
N_LEVELS = 8
PER_LEVEL = 8
MAX_CLUES = 9
ATTEMPTS = 40
PUZZLES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smart_cookies_puzzles.json")

# 每級可用的線索類型與抽取權重（越後面的級別「直接指定位置」越少）
LEVEL_WEIGHTS = [
    {"at": 1},
    {"at": 1, "sat": 2, "cat": 2},
    {"at": 1, "sat": 2, "cat": 2, "nat": 2},
    {"at": 1, "sat": 1.5, "cat": 1.5, "nat": 1.5, "rel": 3},
    {"at": .7, "sat": 1, "cat": 1, "nat": 1, "rel": 2, "row": 2, "col": 2},
    {"at": .5, "sat": 1, "cat": 1, "nat": 1.5, "rel": 1, "row": 1.5, "col": 1.5, "nrow": 2, "ncol": 2},
    {"at": .2, "sat": .8, "cat": .8, "nat": 1.5, "rel": 1, "row": 1.5, "col": 1.5, "nrow": 2, "ncol": 2},
    {"sat": .5, "cat": .5, "nat": 1.5, "rel": 1, "row": 1.5, "col": 1.5, "nrow": 2, "ncol": 2},
]
# 每級新引入的「主打線索」：最小化時最後才嘗試移除，且至少要出現 MIN_FEATURED 條
FEATURED = [("at",), ("sat", "cat"), ("nat",), ("rel",), ("row", "col"), ("nrow", "ncol"), (), ()]
MIN_FEATURED = 2
DISPLAY_RANK = {"at": 0, "sat": 1, "cat": 2, "rel": 3, "row": 4, "col": 5, "nat": 6, "nrow": 7, "ncol": 8}


def shape(k):
    return k // 3


def color(k):
    return k % 3


def row(cell):
    return cell // 3


def col(cell):
    return cell % 3


def all_true_clues(sol):
    """由解答列出所有「為真」的候選線索，依類型分組。sol: tuple 長 9，cell → 餅乾。"""
    clues = {t: [] for t in DISPLAY_RANK}
    for c, k in enumerate(sol):
        clues["at"].append({"t": "at", "k": k, "cell": c})
        clues["sat"].append({"t": "sat", "s": shape(k), "cell": c})
        clues["cat"].append({"t": "cat", "c": color(k), "cell": c})
        clues["nat"].extend({"t": "nat", "k": k, "cell": c2} for c2 in range(9) if c2 != c)
        clues["row"].append({"t": "row", "k": k, "i": row(c)})
        clues["col"].append({"t": "col", "k": k, "i": col(c)})
        clues["nrow"].extend({"t": "nrow", "k": k, "i": i} for i in range(3) if i != row(c))
        clues["ncol"].extend({"t": "ncol", "k": k, "i": i} for i in range(3) if i != col(c))
        if col(c) < 2:
            clues["rel"].append({"t": "rel", "a": k, "b": sol[c + 1], "d": "L"})
        if row(c) < 2:
            clues["rel"].append({"t": "rel", "a": k, "b": sol[c + 3], "d": "U"})
    return clues


def check(clue, grid, pos):
    """對部分填好的盤面判斷線索：True 成立／False 已違反／None 未定。
    grid: tuple 長 9（None＝空格）；pos: 餅乾 → 格子。"""
    t = clue["t"]
    if t == "at":
        if clue["k"] in pos:
            return pos[clue["k"]] == clue["cell"]
        return None if grid[clue["cell"]] is None else False
    if t == "sat":
        g = grid[clue["cell"]]
        return None if g is None else shape(g) == clue["s"]
    if t == "cat":
        g = grid[clue["cell"]]
        return None if g is None else color(g) == clue["c"]
    if t == "nat":
        if clue["k"] in pos:
            return pos[clue["k"]] != clue["cell"]
        return None if grid[clue["cell"]] is None else True
    if t == "rel":
        return _check_rel(clue, grid, pos)
    axis = row if t in ("row", "nrow") else col
    if clue["k"] in pos:
        hit = axis(pos[clue["k"]]) == clue["i"]
        return hit if t in ("row", "col") else not hit
    if t in ("row", "col"):
        line = [c for c in range(9) if axis(c) == clue["i"]]
        return False if all(grid[c] is not None for c in line) else None
    return None


def _check_rel(clue, grid, pos):
    a, b, step = clue["a"], clue["b"], (1 if clue["d"] == "L" else 3)
    edge = col if clue["d"] == "L" else row
    if a in pos:
        if edge(pos[a]) == 2:
            return False
        cb = pos[a] + step
        if b in pos:
            return pos[b] == cb
        return None if grid[cb] is None else False
    if b in pos:
        if edge(pos[b]) == 0:
            return False
        return None if grid[pos[b] - step] is None else False
    return None


def count_solutions(clues, grid=(None,) * 9, limit=2):
    """回溯計數解答數，最多數到 limit 就停。"""
    if None not in grid:
        return 1
    cell = grid.index(None)
    pos = {k: i for i, k in enumerate(grid) if k is not None}
    total = 0
    for k in range(9):
        if k in pos:
            continue
        g2 = grid[:cell] + (k,) + grid[cell + 1:]
        p2 = {**pos, k: cell}
        if all(check(cl, g2, p2) is not False for cl in clues):
            total += count_solutions(clues, g2, limit - total)
            if total >= limit:
                return total
    return total


def _pick_until_unique(avail, weights, rng):
    """依權重抽線索直到只剩唯一解。avail: 類型 → 候選列表（不修改原物件）。"""
    chosen = []
    while count_solutions(chosen) > 1:
        types = [t for t in avail if avail[t]]
        t = rng.choices(types, [weights[t] for t in types])[0]
        chosen = chosen + [avail[t][0]]
        avail = {**avail, t: avail[t][1:]}
    return chosen


def _minimize(chosen, featured, rng):
    """逐條嘗試移除仍保持唯一解的線索；主打類型排最後，較可能留下。"""
    keep = chosen
    order = rng.sample(chosen, len(chosen))
    order = [c for c in order if c["t"] not in featured] + [c for c in order if c["t"] in featured]
    for cl in order:
        trial = [c for c in keep if c is not cl]
        if count_solutions(trial) == 1:
            keep = trial
    return keep


def generate_puzzle(level, rng):
    weights, featured = LEVEL_WEIGHTS[level], FEATURED[level]
    best = None
    for _ in range(ATTEMPTS):
        sol = tuple(rng.sample(range(9), 9))
        pool = all_true_clues(sol)
        avail = {t: rng.sample(pool[t], len(pool[t])) for t in weights}
        clues = _minimize(_pick_until_unique(avail, weights, rng), featured, rng)
        n_feat = sum(1 for c in clues if c["t"] in featured)
        good = (not featured or n_feat >= MIN_FEATURED) and len(clues) <= MAX_CLUES
        score = (0 if good else 1, len(clues))  # 先求達標，再求線索少
        if best is None or score < best[0]:
            best = (score, sol, clues)
        if good:
            break
    _, sol, clues = best
    clues = sorted(clues, key=lambda c: DISPLAY_RANK[c["t"]])
    return {"lv": level + 1, "sol": list(sol), "clues": clues}


def generate_all(seed=SEED):
    rng = random.Random(seed)
    return [generate_puzzle(lv, rng) for lv in range(N_LEVELS) for _ in range(PER_LEVEL)]


def load_puzzles():
    """讀取（或首次生成並寫入）題庫。"""
    if not os.path.exists(PUZZLES_PATH):
        puzzles = generate_all()  # 先算完再開檔，避免中途出錯留下空檔
        with open(PUZZLES_PATH, "w", encoding="utf-8") as f:
            json.dump(puzzles, f, ensure_ascii=False, separators=(",", ":"))
    with open(PUZZLES_PATH, encoding="utf-8") as f:
        puzzles = json.load(f)
    if len(puzzles) != N_LEVELS * PER_LEVEL:
        raise ValueError(f"題庫應有 {N_LEVELS * PER_LEVEL} 題，實際 {len(puzzles)}")
    return puzzles


def verify(puzzles):
    """每題必須恰有唯一解且等於 sol；回傳每級線索數統計。"""
    stats = {}
    for i, p in enumerate(puzzles):
        if count_solutions(p["clues"]) != 1:
            raise AssertionError(f"第 {i + 1} 題不是唯一解")
        pos = {k: c for c, k in enumerate(p["sol"])}
        if not all(check(cl, tuple(p["sol"]), pos) for cl in p["clues"]):
            raise AssertionError(f"第 {i + 1} 題線索與解答矛盾")
        types = {}
        for cl in p["clues"]:
            types[cl["t"]] = types.get(cl["t"], 0) + 1
        stats.setdefault(p["lv"], []).append((len(p["clues"]), types))
    return stats


if __name__ == "__main__":
    import time
    t0 = time.time()
    stats = verify(load_puzzles())
    for lv, rows in stats.items():
        print(f"Level {lv}: 線索數 {[n for n, _ in rows]}")
        for n, types in rows:
            print("   ", types)
    print(f"ok, {time.time() - t0:.1f}s")
