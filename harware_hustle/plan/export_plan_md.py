"""Writes BUILD_PLAN.md: the whole build book as Markdown, readable without a browser and by future Claude sessions.

build_page.py calls write() after it renders the page, so the file always matches the published book.
"""
import datetime as dt
import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "div", "ul", "ol", "li", "table", "dl", "dt", "dd", "pre", "h1", "h2", "h3", "h4", "h5", "h6", "section",
         "article", "header", "footer", "main", "figure", "figcaption", "details", "summary", "blockquote", "nav", "tr",
         "td", "th", "thead", "tbody", "aside", "form", "hr"}
SKIP_TAGS = {"script", "style", "button", "select", "textarea", "nav", "title", "template"}
SKIP_IDS = {"countdown", "bench-mode", "cal-sync", "chk-mode", "dl-note", "cal-csv-note", "cal-example", "toast"}
SKIP_CLASSES = {"out", "kv", "cmd", "who", "toast"}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.kids, self.parent = tag, dict(attrs), [], parent

    def cls(self):
        return set((self.attrs.get("class") or "").split())

    def all(self, pred):
        out = []
        for k in self.kids:
            if isinstance(k, Node):
                if pred(k):
                    out.append(k)
                out += k.all(pred)
        return out

    def first(self, pred):
        found = self.all(pred)
        return found[0] if found else None


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [], None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def skipped(n):
    return (n.tag in SKIP_TAGS or "hidden" in n.attrs or n.attrs.get("id") in SKIP_IDS or n.cls() & SKIP_CLASSES
            or (n.tag == "svg" and "chart" in n.cls()))


def inline(n):
    if isinstance(n, str):
        return re.sub(r"\s+", " ", n)
    if skipped(n) or n.tag in ("input", "svg"):
        return ""
    inner = "".join(inline(k) for k in n.kids)
    t = n.tag
    if t in ("code", "kbd"):
        return f"`{inner.strip()}`" if inner.strip() else ""
    if t in ("strong", "b"):
        return f"**{inner.strip()}**" if inner.strip() else ""
    if t in ("em", "i"):
        return f"*{inner.strip()}*" if inner.strip() else ""
    if t == "a":
        href = n.attrs.get("href") or ""
        return f"[{inner.strip()}]({href})" if href.startswith("http") else inner
    if t == "sup":
        return "^" + inner
    if t == "sub":
        return "_" + inner
    if t == "br":
        return " "
    if t == "li":
        return " • " + inner
    if t in BLOCK:
        return " " + inner + " "
    return inner


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def cell(n):
    return clean(inline(n)).lstrip("• ").replace("|", "\\|")


def table(n):
    head = [cell(th) for th in n.all(lambda x: x.tag == "th")]
    body = n.first(lambda x: x.tag == "tbody") or n
    rows = [[cell(c) for c in tr.kids if isinstance(c, Node) and c.tag in ("td", "th")]
            for tr in body.all(lambda x: x.tag == "tr")]
    rows = [r for r in rows if r]
    if not rows:
        return ""
    width = max(len(head), max(len(r) for r in rows))
    head = head or [""] * width
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r + [""] * (width - len(r))) + " |" for r in rows]
    return "\n".join(out)


def lst(n, depth=0):
    out, k = [], 0
    for li in n.kids:
        if not (isinstance(li, Node) and li.tag == "li"):
            continue
        k += 1
        text = clean("".join(inline(c) for c in li.kids if not (isinstance(c, Node) and c.tag in ("ul", "ol"))))
        mark = f"{k}." if n.tag == "ol" else "-"
        out.append("  " * depth + f"{mark} {text}")
        for sub in li.kids:
            if isinstance(sub, Node) and sub.tag in ("ul", "ol"):
                out.append(lst(sub, depth + 1))
    return "\n".join(out)


def svg_text(svg):
    words = []
    for t in svg.all(lambda x: x.tag == "text"):
        s = clean("".join(k if isinstance(k, str) else "" for k in t.kids))
        if s and (not words or words[-1] != s):
            words.append(s)
    return " · ".join(words)


def fields(n):
    pairs = []
    for f in n.all(lambda x: "field" in x.cls()):
        lab = f.first(lambda x: x.tag == "label")
        inp = f.first(lambda x: x.tag == "input")
        if lab and inp and inp.attrs.get("value"):
            pairs.append(f"{clean(inline(lab))} = {inp.attrs['value']}")
    return ("Inputs and their defaults: " + "; ".join(pairs) + ".") if pairs else ""


class Writer:
    def __init__(self, checks, extras):
        self.checks, self.extras = checks, extras

    def blocks(self, n):
        out, buf = [], []

        def flush():
            s = clean("".join(buf))
            if s:
                out.append(s)
            buf.clear()

        for k in n.kids:
            if isinstance(k, str) or (k.tag not in BLOCK and k.tag != "svg" and not skipped(k) and "tag" not in k.cls()):
                buf.append(inline(k))
            else:
                flush()
                r = self.block(k)
                if r:
                    out.append(r)
        flush()
        text = ""
        for i, r in enumerate(out):
            tight = i and r.startswith("- ") and out[i - 1].split("\n")[-1].lstrip().startswith("- ")
            text += ("\n" if tight else "\n\n") + r if i else r
        return text

    def block(self, n):
        r = self._block(n)
        extra = self.extras.get(n.attrs.get("id"))
        return f"{r}\n\n{extra}" if r and extra else r

    def _block(self, n):
        if skipped(n):
            return ""
        t, c, nid = n.tag, n.cls(), n.attrs.get("id")
        if nid == "checks":
            return "\n\n".join(f"### {g['title']}\n\n" + "\n".join(f"- [ ] {clean(inline(parse(i[1])))}" for i in g["items"])
                               for g in self.checks)
        if t in ("h1", "h2", "h3"):
            return "#" * int(t[1]) + " " + clean(inline(n))
        if t in ("h4", "h5", "h6"):
            return f"**{clean(inline(n))}**"
        if t == "p":
            s = clean(inline(n))
            if not s:
                return ""
            if "eyebrow" in c:
                return f"*{s}*"
            return f"> {s}" if "banner" in c else s
        if t in ("ul", "ol"):
            return lst(n)
        if t == "table":
            return table(n)
        if t == "dl":
            out = []
            for dt_ in n.all(lambda x: x.tag == "dt"):
                dd = dt_.parent.kids[dt_.parent.kids.index(dt_) + 1:]
                dd = next((x for x in dd if isinstance(x, Node) and x.tag == "dd"), None)
                val = clean(inline(dd)) if dd is not None and not skipped(dd) else ""
                if val:
                    out.append(f"- **{clean(inline(dt_))}:** {val}")
            return "\n".join(out)
        if t == "pre":
            raw = "".join(k if isinstance(k, str) else "" for k in n.kids).strip("\n")
            return f"```\n{raw}\n```"
        if t == "svg":
            label = n.attrs.get("aria-label", "")
            words = svg_text(n)
            return f"**Diagram:** {label}" + (f"\n\n*Text in the drawing:* {words}" if words else "")
        if t == "figcaption":
            s = clean(inline(n))
            return f"*{s}*" if s else ""
        if t == "details":
            return "" if n.first(lambda x: x.tag == "textarea") else self.blocks(n)
        if "sheet-head" in c:
            eb = n.first(lambda x: "eyebrow" in x.cls())
            h2 = n.first(lambda x: x.tag == "h2")
            ledes = [clean(inline(p)) for p in n.kids if isinstance(p, Node) and p.tag == "p" and "eyebrow" not in p.cls()]
            head = f"## {clean(inline(eb))}: {clean(inline(h2))}" if eb else f"## {clean(inline(h2))}"
            return "\n\n".join([head] + [x for x in ledes if x])
        if "runsheet" in c:
            cells = [cell(k) for k in n.kids if isinstance(k, Node)]
            ncol = sum(1 for k in n.kids if isinstance(k, Node) and "hd" in k.cls())
            rows = [cells[i:i + ncol] for i in range(0, len(cells), ncol)]
            return "\n".join(["| " + " | ".join(rows[0]) + " |", "|" + "---|" * ncol] +
                             ["| " + " | ".join(r) + " |" for r in rows[1:]])
        if "finding" in c:
            parts = [k for k in n.kids if isinstance(k, Node)]
            dec = parts[2].first(lambda x: "dec" in x.cls())
            src = parts[2].first(lambda x: "src" in x.cls())
            return f"- {clean(inline(parts[0]))} → **{clean(inline(dec))}** ({clean(inline(src))})"
        if t == "article" and ("ms" in c or "role" in c):
            hid = clean(inline(n.first(lambda x: "id" in x.cls())))
            h3 = clean(inline(n.first(lambda x: x.tag == "h3")))
            holder = Node("div", [], None)
            holder.kids = [k for k in n.kids if not (isinstance(k, Node) and k.tag == "header")]
            return f"### {hid} · {h3}\n\n{self.blocks(holder)}"
        if "chips" in c:
            return "*" + " · ".join(clean(inline(k)) for k in n.kids if isinstance(k, Node)) + "*"
        if "citem" in c:
            lab = n.first(lambda x: x.tag == "label")
            return f"- [ ] {clean(inline(lab))}" if lab else ""
        if "fields" in c:
            return fields(n)
        if "field" in c:
            return fields(_wrap(n))
        if "tool" in c:
            hdr = n.first(lambda x: x.tag == "header")
            rest = [k for k in n.kids if k is not hdr]
            title = clean(inline(hdr.first(lambda x: x.tag == "h3"))) if hdr else ""
            note = hdr.first(lambda x: "note" in x.cls() and not skipped(x)) if hdr else None
            holder = Node("div", [], None)
            holder.kids = rest
            head = f"### Tool: {title}" + (f"\n\n{clean(inline(note))}" if note is not None and clean(inline(note)) else "")
            return head + "\n\n" + self.blocks(holder)
        if "tag" in c and t == "span":
            return f"**{clean(inline(n))}**"
        return self.blocks(n)


def _wrap(n):
    h = Node("div", [], None)
    h.kids = [n]
    return h


def parse(fragment):
    tr = Tree()
    tr.feed(fragment)
    tr.close()
    return tr.root


def write(page_html, checks, path, preamble, extras):
    root = parse(page_html)
    w = Writer(checks, extras)
    parts = [preamble.rstrip()]
    hdr = root.first(lambda x: x.tag == "header" and "wrap" in x.cls())
    tb = hdr.first(lambda x: "tb-grid" in x.cls())
    lede = hdr.first(lambda x: "lede" in x.cls())
    parts.append("## Title block\n\n" + clean(inline(lede)) + "\n\n" + w.block(tb))
    parts.append("## Contract\n\n" + w.blocks(hdr.first(lambda x: "contract" in x.cls())))
    for sec in root.all(lambda x: x.tag == "section" and "sheet" in x.cls()):
        parts.append(w.block(sec))
    text = "\n\n".join(p for p in parts if p).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    open(path, "w", encoding="utf-8").write(text)
    return text


def velocity_table(theory_dir):
    sys.path.insert(0, theory_dir)
    import theory

    rows = ["| Flow (L/min) | v at 8 mm (m/s) | Re | v at 5 mm bore (m/s) | Re | Regime at 5 mm | Δp at 5 mm (kPa/m) | 1 m transit (s) |",
            "|---|---|---|---|---|---|---|---|"]
    for q in (1.0, 3.0, 6.0):
        v8, re8, _, _, _ = theory.row(q, 8.0, 1.0)
        v5, re5, reg5, dpl5, tt5 = theory.row(q, 5.0, 1.0)
        rows.append(f"| {q:.0f} | {v8:.3f} | {re8:.0f} | {v5:.3f} | {re5:.0f} | {reg5} | {dpl5 / 1000:.2f} | {tt5:.2f} |")
    return ("Theory at the paper's 8 mm and the measured-bore assumption of 5 mm (from `tools/theory.py`; rerun it with "
            "the measured bore and achieved flows):\n\n" + "\n".join(rows))


def stamp():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":
    sys.exit("run build_page.py; it calls write()")
