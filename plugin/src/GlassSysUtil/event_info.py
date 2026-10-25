"""Open ECM information through the receiver's existing Extensions menu."""


def open_ecm(session, servicelist=None, **kwargs):
    # Import on selection: the plugin module defines ECMInfo after Plugins().
    from .plugin import ECMInfo
    session.open(ECMInfo)
