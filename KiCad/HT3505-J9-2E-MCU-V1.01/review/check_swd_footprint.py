from pathlib import Path
import pcbnew
root=Path(__file__).resolve().parents[1]
name='SWD_Pads_1x05_P1.27mm_0.8x1.5mm_NoPaste'
fp=pcbnew.FootprintLoad(str(root/'Motor_Interfaces.pretty'),name)
assert fp is not None
pads=sorted(fp.Pads(),key=lambda p:int(p.GetNumber()))
assert len(pads)==5
for i,p in enumerate(pads):
    assert p.GetNumber()==str(i+1)
    assert abs(pcbnew.ToMM(p.GetPosition().x)-(i-2)*1.27)<1e-6
    assert pcbnew.ToMM(p.GetPosition().y)==0
    assert pcbnew.ToMM(p.GetSize().x)==0.8 and pcbnew.ToMM(p.GetSize().y)==1.5
    assert p.GetLayerSet().Contains(pcbnew.F_Mask)
    assert not p.GetLayerSet().Contains(pcbnew.F_Paste)
print('PASS: KiCad load; pins 1-5; 1.27 mm pitch; 0.8 x 1.5 mm pads; mask enabled, paste disabled.')
