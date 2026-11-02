"""Fit only this plugin's native vertical lists; no global image patches."""
from Screens.Screen import Screen as NativeScreen
from enigma import eListbox, eSize


def fit(component, listbox=eListbox, make_size=eSize):
    instance = getattr(component, 'instance', None)
    if not isinstance(instance, listbox):
        return False
    try:
        if instance.getOrientation() != listbox.orVertical:
            return False
        attributes = dict(getattr(component, 'skinAttributes', None) or ())
        if any(int(part.strip()) for part in attributes.get('itemSpacing', '0,0').split(',')):
            return False
        size = instance.size()
        current = (size.width(), size.height())
        previous = getattr(component, '_warder_row_area', None)
        allocated = previous[1] if previous and previous[0] is instance and current in previous[1:] else current
        row = int(instance.getItemHeight())
        if row <= 0 or allocated[0] <= 0 or allocated[1] < row:
            return False
        target = (allocated[0], allocated[1] // row * row)
        if current != target:
            instance.resize(make_size(*target))
        component._warder_row_area = (instance, allocated, target)
        return current != target
    except (AttributeError, TypeError, ValueError):
        return False


class Screen(NativeScreen):
    def fit_lists(self):
        for component in self.values():
            fit(component)

    def applySkin(self):
        result = NativeScreen.applySkin(self)
        # Native layout callbacks have now applied their final content heights.
        self.fit_lists()
        return result

    def show(self):
        result = NativeScreen.show(self)
        self.fit_lists()
        return result
