# -*- coding: utf-8 -*-
"""書籍自動註冊：掃描 book_<slug>.py 模組（book_common 除外），依 BOOK['order'] 排序。
新書＝新增一個 book_<slug>.py 並匯出 BOOK dict，不需要改本檔。"""
import glob
import importlib


def load_books():
    books = []
    for f in sorted(glob.glob("book_*.py")):
        name = f[:-3]
        if name == "book_common":
            continue
        mod = importlib.import_module(name)
        book = getattr(mod, "BOOK", None)
        if book is None:
            raise ValueError(f"{name}.py 缺少 BOOK dict")
        for key in ("slug", "order", "title_pre", "title_hi", "title_post", "title_zh",
                    "subtitle", "tagline_zh", "chips", "pdf_name", "bg", "pages",
                    "parent_tips", "parent_intro", "cue_html", "cover"):
            if key not in book:
                raise ValueError(f"{name}.BOOK 缺少欄位 {key}")
        books.append(book)
    return sorted(books, key=lambda b: b["order"])
