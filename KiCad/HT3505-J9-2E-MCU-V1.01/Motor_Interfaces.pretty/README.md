# Project interface footprints

Library nickname: `Motor_Interfaces` (registered in project fp-lib-table).

## SWD_Pads_1x05_P1.27mm_0.8x1.5mm_NoPaste

Five pads in one row, 1.27 mm center spacing, each 0.80 x 1.50 mm copper. Copper envelope 5.88 x 1.50 mm. Pad 1 is marked by a silk triangle at the left in component-side view. F.Cu/F.Mask only, mask expansion 0.05 mm; no paste. No component to assemble.

Assign to Conn_01x05. Suggested custom mapping: 1=3V3/VTref, 2=SWDIO, 3=GND, 4=SWCLK, 5=NRST. The footprint contains only pad numbers, so check the actual schematic mapping before making the cable or fixture. This is NOT the standard ARM 2x5 pinout and is NOT compatible with a Tag-Connect cable. Standard 1.27 mm pitch alone does not imply a standard cable pinout.

Use board tooling holes or a board-outline fixture for pogo alignment; no locating holes are imposed by this footprint. Keep probe faces free of open vias and solder for production, use suitable probe diameter/stroke and ENIG finish where practical. Use short flying wires for development; remove residual solder before probing a previously hand-soldered board. VTref is a target-voltage reference unless a separate target-power scheme is explicitly provided.

## ZX_SH1.0_3PWT_1x03_P1.00mm_Horizontal

Source: user-supplied ZX-SH1.0-3PWT drawing, revision 2.0. The generic six-contact layout is reduced to three contacts using A=2.00, B=5.35, C=3.60 mm from its table.

- Component-side view; signal tails at top, mating opening toward bottom.
- Signal pads: 0.50 x 1.70 mm; 1.00 mm pitch.
- Signal pad centers: (-1,0), (0,0), (1,0) mm.
- Mechanical pads: 1.20 x 2.50 mm at (-2.10,3.40), (2.10,3.40) mm; unnumbered, not assigned to GND.
- Overall land envelope: 5.40 x 5.50 mm.
- Body width/depth: 5.35 x 4.30 mm. Body position relative to lands is approximate because the screenshot does not fully dimension that offset; electrical land coordinates follow the layout dimensions.
- Nominal component height: 3.15 +/- 0.20 mm. Not compatible with a total 3.1 mm assembly-height limit without mechanical accommodation.
- Pin numbers 1-3 left-to-right are a PROJECT CONVENTION: the supplied drawing does not specify electrical pin numbering. Match the cable wiring to the marked pad 1; do not assume a vendor harness numbering convention.
- No 3D model supplied. Allow additional board-edge space for the mating plug and wire bend.

## WirePad_1P_1.5x1.5mm_NoPaste / WirePad_1P_2.0x2.0mm_NoPaste

- One square SMD copper pad, pin 1, centered at origin.
- Copper dimensions exactly 1.50 x 1.50 / 2.00 x 2.00 mm.
- F.Cu and F.Mask only; no F.Paste. Mask expansion 0.05 mm each side.
- Excluded from placement files and footprint BOM because no component is installed.
- Assign to `Connector_Generic:Conn_01x01` (or another symbol with one pin numbered 1).
- Each schematic instance is independently movable on PCB. Copper routing and mechanical strain relief determine usable current and durability; pad size alone does not establish a current rating.

Validation: all three files loaded successfully using KiCad 10 pcbnew; pad counts, centers, sizes and single-pad paste exclusion checked. Verification board is in `review/interface-footprints-check.kicad_pcb`.
