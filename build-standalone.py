"""Build preview.html: index.html with every image inlined, so it works in
previews that cannot load relative files. index.html stays the source for GitHub."""
import base64, glob, json, os, re

root = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(root, "index.html"), encoding="utf-8").read()

def uri(path):
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(os.path.join(root, path), "rb").read()).decode())

# static banner backgrounds
html = re.sub(r"url\((img/banners/[\w-]+\.jpg)\)", lambda m: "url(%s)" % uri(m.group(1)), html)

# covers and team photos are looked up by the I() helper
found = sorted(glob.glob(os.path.join(root, "img/covers/*.jpg")) + glob.glob(os.path.join(root, "img/team/*.jpg")))
imgs = {os.path.relpath(f, root): uri(os.path.relpath(f, root)) for f in found}
inject = "<script>window.IMG=%s;</script>\n" % json.dumps(imgs)
html = html.replace("<script>\n// image path helper", inject + "<script>\n// image path helper", 1)

open(os.path.join(root, "preview.html"), "w", encoding="utf-8").write(html)
print("preview.html", round(len(html) / 1e6, 1), "MB,", len(imgs), "images inlined")
