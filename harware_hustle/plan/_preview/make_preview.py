import sys; sys.path.insert(0,'..')
import diagrams as D
css = D.PRINT_CSS.replace('svg{','svg.diagram{')
html = "<html><head><meta charset='utf-8'><style>body{margin:0;background:#fff}"+css+" svg.diagram{display:block;width:1280px;height:auto;margin:0 0 30px}</style></head><body>"
for f in (D.pid, D.power, D.conditioning, D.states):
    html += f()
html += "</body></html>"
open('all.html','w').write(html)
