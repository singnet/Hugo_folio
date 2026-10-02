import re, sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src).read().split("\n")

def esc(s):
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

pages, cur = [], []
for ln in lines:
    cur.append(ln)
    if len(cur) >= 45:
        pages.append(cur); cur = []
if cur: pages.append(cur)

content_streams = []
for pg in pages:
    stream = "BT /F1 11 Tf 12 780 Td 14 TL\n"
    for ln in pg:
        stream += "(" + esc(ln) + ") Tj T*\n"
    stream += "ET"
    content_streams.append(stream)

buf = bytearray()
offsets = []
def add_obj(body):
    offsets.append(len(buf))
    buf.extend(("%d 0 obj\n" % (len(offsets) + 1)).encode())
    buf.extend(body.encode())
    buf.extend(b"\nendobj\n")

n = len(pages)
pages_obj_num = 2
font_obj_num = 3
first_page = 4
first_content = 4 + n
kids = " ".join("%d 0 R" % (first_page + i) for i in range(n))
add_obj("<< /Type /Catalog /Pages %d 0 R >>" % pages_obj_num)
add_obj("<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, n))
add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
for i in range(n):
    add_obj("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>" % (pages_obj_num, font_obj_num, first_content + i))
for s in content_streams:
    add_obj("<< /Length %d >>\nstream\n%s\nendstream" % (len(s.encode()), s))

xref_pos = len(buf)
buf.extend(("xref\n0 %d\n0000000000 65535 f \n" % (len(offsets) + 1)).encode())
for off in offsets:
    buf.extend(("%010d 00000 n \n" % off).encode())
buf.extend(("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF" % (len(offsets) + 1, xref_pos)).encode())
open(dst, "wb").write(bytes(buf))
print("WROTE", dst, "pages:", n)