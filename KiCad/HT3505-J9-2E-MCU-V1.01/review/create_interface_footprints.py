from pathlib import Path
import pcbnew

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'Motor_Interfaces.pretty'
LIB.mkdir(exist_ok=True)

def line(x1,y1,x2,y2,layer='F.SilkS',width=.12):
    return f'(fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (layer "{layer}"))'

def rect(x1,y1,x2,y2,layer,width):
    return f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))'

def make(name,desc,items,refy,valy,virtual=False):
    text = f'''(footprint "{name}" (version 20241229) (generator "pcbnew")
    (layer "F.Cu") (descr "{desc}")
    (attr smd {'exclude_from_pos_files exclude_from_bom' if virtual else ''})
    (fp_text reference "REF**" (at 0 {refy}) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "{name}" (at 0 {valy}) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
    {chr(10).join(items)}
    )'''
    (LIB / (name+'.kicad_mod')).write_text(text,encoding='utf-8')

for size in (1.5,2.0):
    h=size/2
    name=f'WirePad_1P_{size:.1f}x{size:.1f}mm_NoPaste'
    make(name,'Single square copper solder pad; pin 1; no paste aperture; dimensions are copper size',[
        f'(pad "1" smd rect (at 0 0) (size {size} {size}) (layers "F.Cu" "F.Mask") (solder_mask_margin 0.05))',
        rect(-h,-h,h,h,'F.Fab',.1),
        rect(-h-.25,-h-.25,h+.25,h+.25,'F.CrtYd',.05)
    ],-h-.8,h+.8,True)

# Supplied ZX-SH1.0-3PWT drawing, component-side view, tails at top.
# Signal row centered at origin. Drawing total land depth 5.50;
# signal lands 0.50 x 1.70; hold-down lands 1.20 x 2.50.
items=[]
for i,x in enumerate((-1,0,1),1):
    items.append(f'(pad "{i}" smd rect (at {x} 0) (size 0.5 1.7) (layers "F.Cu" "F.Paste" "F.Mask"))')
for x in (-2.1,2.1):
    items.append(f'(pad "" smd rect (at {x} 3.4) (size 1.2 2.5) (layers "F.Cu" "F.Paste" "F.Mask"))')
items += [rect(-2.675,-.05,2.675,4.25,'F.Fab',.1),
          rect(-2.95,-1.1,2.95,4.9,'F.CrtYd',.05),
          line(-2.8,.1,-2.8,1.85),line(2.8,.1,2.8,1.85),
          line(-1.25,4.4,1.25,4.4),
          '(fp_poly (pts (xy -1 -1.1) (xy -1.2 -1.45) (xy -0.8 -1.45)) (stroke (width 0.1) (type default)) (fill solid) (layer "F.SilkS"))']
make('ZX_SH1.0_3PWT_1x03_P1.00mm_Horizontal',
     'ZX-SH1.0-3PWT per supplied drawing; 3.15mm nominal height; top view left-to-right pins 1-3 (project convention); body outline placement approximate; unnumbered isolated hold-down pads',items,-2,5.5)

for p in sorted(LIB.glob('*.kicad_mod')):
    fp=pcbnew.FootprintLoad(str(LIB),p.stem)
    assert fp is not None,p
    pads=list(fp.Pads())
    expected=5 if p.name.startswith('ZX_') else 1
    assert len(pads)==expected,(p,len(pads))
    for pad in pads:
        if expected==1:
            assert not pad.GetLayerSet().Contains(pcbnew.F_Paste)
        print(p.stem, 'pad',repr(pad.GetNumber()),'xy',pcbnew.ToMM(pad.GetPosition().x),pcbnew.ToMM(pad.GetPosition().y),'size',pcbnew.ToMM(pad.GetSize().x),pcbnew.ToMM(pad.GetSize().y))

# Plot from KiCad's parsed footprint geometry for visual inspection.
board=pcbnew.BOARD()
for name,x,y in [('ZX_SH1.0_3PWT_1x03_P1.00mm_Horizontal',30,30),('WirePad_1P_1.5x1.5mm_NoPaste',42,30),('WirePad_1P_2.0x2.0mm_NoPaste',50,30)]:
    fp=pcbnew.FootprintLoad(str(LIB),name)
    board.Add(fp)
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
pcbnew.SaveBoard(str(ROOT/'review/interface-footprints-check.kicad_pcb'),board)
print('KiCad loaded all three footprints and saved verification board.')
