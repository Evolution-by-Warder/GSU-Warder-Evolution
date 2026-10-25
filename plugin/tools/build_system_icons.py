"""Build retained transparent Warder status icons; no receiver-side graphics dependency."""
from pathlib import Path
import cairosvg

BASE=Path(__file__).resolve().parents[1]
SHAPES={}


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
