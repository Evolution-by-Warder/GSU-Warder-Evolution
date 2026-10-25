"""Build transparent Warder vector icons; no receiver-side graphics dependency."""
from pathlib import Path
import cairosvg

BASE=Path(__file__).resolve().parents[1]
SHAPES={
'mem':'<rect x="8" y="20" width="48" height="24" rx="3"/><path d="M16 44v7m8-7v7m8-7v7m8-7v7m8-7v7"/><path d="M16 27h10v10H16zm22 0h10v10H38z"/>',
'swap':'<path d="M12 25a21 21 0 0 1 36-9l5 5M53 10v11H42M52 39a21 21 0 0 1-36 9l-5-5M11 54V43h11"/>',
'summ':'<rect x="17" y="9" width="38" height="30" rx="4"/><rect x="9" y="25" width="38" height="30" rx="4"/><path d="M17 35h22m-22 9h16"/>',
'root':'<rect x="12" y="8" width="40" height="48" rx="5"/><path d="M12 44h40M37 18 27 35"/><circle cx="44" cy="50" r="1"/>',
'hdd':'<rect x="10" y="7" width="44" height="50" rx="5"/><circle cx="32" cy="28" r="13"/><circle cx="32" cy="28" r="3"/><path d="m44 15-12 13M10 47h44m-10 5h1"/>',
'usb':'<path d="M23 24V9h18v15M22 24h20v27l-5 6H27l-5-6zM29 14v5m6-5v5M28 34h8v10h-8z"/>',
'cf':'<rect x="10" y="9" width="44" height="46" rx="4"/><path d="M18 12v6m7-6v6m7-6v6m7-6v6m7-6v6M18 29h28v16H18zM22 34h8m-8 6h8m8-6h5m-5 0v9"/>',
'sd':'<path d="M22 7h28v50H14V16zM23 9v11m8-11v11m8-11v11m-16 9h18v18H23z"/>',
'hdd_temp':'<rect x="6" y="12" width="32" height="43" rx="4"/><circle cx="22" cy="29" r="10"/><path d="M6 44h26M47 34V12a5 5 0 0 1 10 0v22a10 10 0 1 1-10 0M52 20v22"/>',
'cpu':'<rect x="16" y="16" width="32" height="32" rx="4"/><rect x="24" y="24" width="16" height="16" rx="2"/><path d="M23 7v9m9-9v9m9-9v9M23 48v9m9-9v9m9-9v9M7 23h9m-9 9h9m-9 9h9m32-18h9m-9 9h9m-9 9h9"/>',
'sensor':'<path d="M18 39V12a6 6 0 0 1 12 0v27a11 11 0 1 1-12 0M24 20v27M39 21c11 5 11 17 0 22m6-29c18 9 18 27 0 36"/>',
'lr':'<path d="m24 15-17 17 17 17m16-34 17 17-17 17M8 32h48"/>',
'updown':'<path d="M15 24 32 7l17 17M15 40l17 17 17-17M32 8v48"/>',
}


def build():
    masters=BASE/'artwork/system-icons';masters.mkdir(parents=True,exist_ok=True)
    output=BASE/'src/GlassSysUtil/images'
    for name,shape in SHAPES.items():
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 64 64"><defs><linearGradient id="metal" x2="0" y2="1"><stop stop-color="#f6fcff"/><stop offset=".5" stop-color="#85d9ef"/><stop offset="1" stop-color="#24bde8"/></linearGradient></defs><g fill="none" stroke="#146887" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'+shape+'</g><g fill="none" stroke="url(#metal)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'+shape+'</g></svg>'
        source=masters/(name+'.svg');source.write_text(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(output/('system-'+name+'.png')))
    for name,color in [('green','#39ff59'),('red','#ff526a')]:
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 64 64"><circle cx="32" cy="32" r="23" fill="'+color+'"/><circle cx="27" cy="25" r="7" fill="#ffffff" opacity=".25"/></svg>'
        source=masters/('status-'+name+'.svg');source.write_text(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=str(output/('system-status-'+name+'.png')))

if __name__=='__main__':build()
