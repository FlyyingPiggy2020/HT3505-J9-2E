import re,json,math
from pathlib import Path
p=Path(__file__).resolve().parents[1]
s=(p/'HT3505-J9-2E-MCU-V1.01.kicad_sch').read_text(encoding='utf-8')
tokens=iter(re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s))
def parse():
    out=[]
    for t in tokens:
        if t==')':return out
        out.append(parse() if t=='(' else json.loads(t) if t.startswith('"') else t)
    return out
root=parse()[0]
def children(n,k):return [v for v in n if isinstance(v,list) and v and v[0]==k]
def one(n,k):return next(iter(children(n,k)),[k])
def xy(n):return tuple(round(float(v),5) for v in n[1:3])
libs={v[1]:v for v in children(one(root,'lib_symbols'),'symbol')}
points={}; parent={}
def add(pt,item=None):
    parent.setdefault(pt,pt)
    if item:points.setdefault(pt,[]).append(item)
def find(x):
    if parent[x]!=x:parent[x]=find(parent[x])
    return parent[x]
def union(a,b):parent[find(a)]=find(b)
wires=[]
for w in children(root,'wire'):
    a,b=[xy(v) for v in children(one(w,'pts'),'xy')];add(a);add(b);union(a,b);wires.append((a,b))
named={}
for kind in ['label','global_label','hierarchical_label']:
    for v in children(root,kind):
        pt=xy(one(v,'at'));add(pt,'NET '+v[1]);named.setdefault(v[1],[]).append(pt)
for sym in children(root,'symbol'):
    props={v[1]:v[2] for v in children(sym,'property')}
    ref=props.get('Reference','?');value=props.get('Value','?')
    origin=xy(one(sym,'at')); angle=float(one(sym,'at')[3]);ang=math.radians(angle)
    lib=libs[one(sym,'lib_id')[1]]
    for block in children(lib,'symbol'):
        for pin in children(block,'pin'):
            x,y=xy(one(pin,'at'));mirror=one(sym,'mirror')[1:]
            if 'x' in mirror:y=-y
            if 'y' in mirror:x=-x
            pt=(round(origin[0]+x*math.cos(ang)-y*math.sin(ang),5),round(origin[1]-x*math.sin(ang)-y*math.cos(ang),5))
            num=one(pin,'number')[1];name=one(pin,'name')[1]
            add(pt,f'{ref}.{num} {name} [{value}]')
            if ref.startswith('#PWR'):named.setdefault(value,[]).append(pt)
for pt in list(parent):
    for a,b in wires:
        cross=(pt[0]-a[0])*(b[1]-a[1])-(pt[1]-a[1])*(b[0]-a[0])
        if abs(cross)<1e-7 and min(a[0],b[0])-1e-6<=pt[0]<=max(a[0],b[0])+1e-6 and min(a[1],b[1])-1e-6<=pt[1]<=max(a[1],b[1])+1e-6:union(pt,a)
for pts in named.values():
    for pt in pts[1:]:union(pts[0],pt)
groups={}
for pt,items in points.items():groups.setdefault(find(pt),[]).extend(items)
for g in groups.values():
    if any(re.match(r'U[356]\.',v) for v in g):print(' | '.join(v for v in g if not v.startswith('#')))
