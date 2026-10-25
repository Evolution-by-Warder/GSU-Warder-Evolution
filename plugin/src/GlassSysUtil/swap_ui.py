"""Keep the original swap screens responsive while worker operations run."""
from .i18n import for_api as _i18n_text
from twisted.internet.threads import deferToThread
from .swap_ops import SwapStore, places, swaps


_SK = {
    'Loading disks...': 'Načítavam disky...',
    'Creating swap...': 'Vytváram swap...',
    'Deleting swap...': 'Odstraňujem swap...',
    'Swap operation failed.': 'Operácia so swapom zlyhala.',
    'Swap partitions cannot be deleted here.': 'Swapové oddiely sa v tejto ponuke nemažú.',
    'No supported writable local disk is mounted.': 'Nie je pripojený podporovaný lokálny disk s možnosťou zápisu.',
}


def tr(api,text):
    return _i18n_text(api,text,_SK)


def init(screen):
    screen._swap_busy = False
    screen._swap_closed = False
    screen.onClose.append(lambda: setattr(screen, '_swap_closed', True))


def exit_screen(screen, api):
    if not screen._swap_busy:
        screen.close()


def error(screen, api, text):
    box = api['MessageBox']
    screen.session.open(box, text, box.TYPE_ERROR)


def load_places(screen, api):
    screen._swap_busy = True
    screen.setTitle(tr(api, 'Loading disks...'))
    def done(paths):
        screen._swap_busy = False
        if screen._swap_closed:
            return
        setting = screen.list[1][1]
        setting.setChoices([api['_']('None')] + paths, default=api['_']('None'))
        screen['config'].invalidateCurrent()
        screen.setTitle(api['_']('Create'))
        if not paths:
            error(screen, api, tr(api, 'No supported writable local disk is mounted.'))
    def failed(failure):
        screen._swap_busy = False
        if not screen._swap_closed:
            screen.setTitle(api['_']('Create'))
            error(screen, api, tr(api, 'Swap operation failed.') + '\n' + str(failure.value))
        return None
    screen._swap_pending = deferToThread(places)
    screen._swap_pending.addCallback(done)
    screen._swap_pending.addErrback(failed)


def run(screen, api, action, *args):
    if screen._swap_busy:
        return
    screen._swap_busy = True
    screen.setTitle(tr(api, 'Creating swap...' if action == 'create' else 'Deleting swap...'))
    def done(path):
        screen._swap_busy = False
        if screen._swap_closed:
            return
        box = api['MessageBox']
        if action == 'create':
            screen.session.openWithCallback(lambda *unused: screen.close(True), box,
                api['_']('Create swapfile finished') + ': ' + path, box.TYPE_INFO, 5)
        else:
            screen.readSwapInfo()
            screen.setTitlenew()
            screen.session.open(box, api['_']('Delete swap') + ': ' + path, box.TYPE_INFO, 5)
    def failed(failure):
        screen._swap_busy = False
        if not screen._swap_closed:
            if action == 'create':
                screen.setTitle(api['_']('Create'))
            else:
                screen.readSwapInfo()
                screen.setTitlenew()
            error(screen, api, tr(api, 'Swap operation failed.') + '\n' + str(failure.value))
        return None
    screen._swap_pending = deferToThread(getattr(SwapStore(), action), *args)
    screen._swap_pending.addCallback(done)
    screen._swap_pending.addErrback(failed)


def create(screen, api):
    if screen._swap_busy:
        return
    size, disk, name = [entry[1].value for entry in screen.list]
    if size == api['_']('None') or disk == api['_']('None') or not name:
        error(screen, api, api['_']('Please set all parameters') + ': ' +
              ', '.join(api['_'](key) for key in ('Size', 'Disk', 'Name')))
        return
    run(screen, api, 'create', disk, int(size), name)


def delete_question(screen, api):
    if screen._swap_busy:
        return
    selected = screen['list'].getCurrent()
    if not selected or selected[0] == 'No swapfile':
        error(screen, api, api['_']('No swapfile for delete'))
        return
    path = selected[0]
    try:
        row = next((row for row in swaps() if row[0] == path), None)
    except OSError as failure:
        error(screen, api, tr(api, 'Swap operation failed.') + '\n' + str(failure))
        return
    if not row or row[1] != 'file':
        error(screen, api, tr(api, 'Swap partitions cannot be deleted here.'))
        return
    screen._swap_delete_path = path
    box = api['MessageBox']
    screen.session.openWithCallback(screen.swapDelete, box,
        api['_']('Really delete swap ?') + '\n' + path, box.TYPE_YESNO, default=False)


def delete(screen, api, answer):
    if answer and getattr(screen, '_swap_delete_path', None):
        path = screen._swap_delete_path
        screen._swap_delete_path = None
        run(screen, api, 'delete', path)


def read_info(screen, api):
    try:
        rows = swaps()
    except (OSError, ValueError) as failure:
        error(screen, api, tr(api, 'Swap operation failed.') + '\n' + str(failure))
        return
    screen.list = []
    scale = api['fhd']
    columns = ((0, 380), (400, 80), (490, 100), (600, 100), (690, 40))
    if not rows:
        rows = [('No swapfile', '****', '****', '****', '****')]
    for row in rows:
        item = [row[0]]
        for index, (left, width) in enumerate(columns):
            text = api['_']('No swapfile') if row[0] == 'No swapfile' and index == 0 else str(row[index])
            item.append(api['MultiContentEntryText'](pos=(scale(left), 0), size=(scale(width), scale(20)), font=0, text=text))
        screen.list.append(item)
    screen['list'].l.setList(screen.list)

