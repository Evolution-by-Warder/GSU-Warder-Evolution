"""Compact the original CAM manager after retiring its color-key shortcut row."""
from xml.etree import ElementTree


def compact_skin(skin):
    root=ElementTree.fromstring(skin)
    rows={node.get('name'):node for node in root if node.tag=='widget'}
    removed=rows.get('txt5')
    if removed is None:return skin
    # Move each following row into its predecessor's exact slot: SD/FHD/UHD
    # use slightly different rounded line spacing.
    previous=removed.get('position')
    root.remove(removed)
    for name in ('txt6','txt7','txt8','txt9'):
        row=rows.get(name)
        if row is not None:
            position=row.get('position')
            row.set('position',previous)
            previous=position
    return ElementTree.tostring(root,encoding='unicode')
