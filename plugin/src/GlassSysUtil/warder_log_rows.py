"""Preserve complete OSCam messages as fixed-height, scrollable colored lines."""
from textwrap import wrap


def rows(entries, build_text, width, font_size, row_height):
    result = []
    columns = max(1, width // max(1, font_size))
    for entry in entries:
        if len(entry) < 2:
            result.append(entry)
            continue
        source = entry[1]
        if isinstance(source, dict):
            text = source.get('text', entry[0])
            colors = {key:source[key] for key in ('color','color_sel','backcolor','backcolor_sel') if key in source}
        else:
            text = source[7]
            colors = {key:source[index] for index,key in enumerate(('color','color_sel','backcolor','backcolor_sel'),8) if index < len(source)}
        # Keep whitespace and explicit newlines, and split unbroken long tokens.
        for paragraph in str(text).split('\n'):
            for line in wrap(paragraph, width=columns, replace_whitespace=False, drop_whitespace=False) or ['']:
                result.append([entry[0], build_text(pos=(0,0),size=(width,row_height),font=1,text=line,**colors)])
    return result
