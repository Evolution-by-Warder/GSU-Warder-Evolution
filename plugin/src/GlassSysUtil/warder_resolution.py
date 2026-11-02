"""Scale legacy XML to the desktop without changing its resource family."""
from xml.etree import ElementTree as ET


def scale_skin(value, base, desktop):
    if base == desktop or not isinstance(value, str) or not value.lstrip().startswith('<screen'):
        return value
    root = ET.fromstring(value)
    sx, sy = desktop[0] / base[0], desktop[1] / base[1]
    for node in root.iter():
        for key in ('position', 'size', 'shadowOffset'):
            if key not in node.attrib:
                continue
            parts = node.get(key).split(',')
            if len(parts) != 2:
                continue
            values = []
            for part, factor in zip(parts, (sx, sy)):
                part = part.strip()
                try:
                    values.append(str(round(int(part) * factor)))
                except ValueError:
                    # Native anchors such as center remain anchors.
                    values.append(part)
            node.set(key, ','.join(values))
        font = node.get('font')
        if font and ';' in font:
            family, points = font.rsplit(';', 1)
            node.set('font', family + ';' + str(max(1, round(int(points) * sy))))
        for key in ('itemHeight', 'borderWidth', 'scrollbarWidth'):
            if key in node.attrib:
                number = int(node.get(key))
                node.set(key, str(max(1, round(number * sy)) if number > 0 else number))
    return ET.tostring(root, encoding='unicode')


def adapt_skins(namespace, base, desktop):
    for name, value in list(namespace.items()):
        if isinstance(value, str) and value.lstrip().startswith('<screen'):
            namespace[name] = scale_skin(value, base, desktop)
