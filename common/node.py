"""
Node Object

Objects that need to be controlled by game systems must inherit this or a
subclass of this.

"""
from kivy.logger import Logger as log  # noqa
from kivy.properties import AliasProperty, BooleanProperty
from kivy.uix.widget import Widget


def ensure_root_node(func):
    def wrapper(*args, **kwargs):
        this = args[0]
        if not this.root_node:
            parent = this.parent
            if parent and hasattr(parent, 'root_node') and parent.root_node:
                this.root_node = parent.root_node
            else:
                for node in this.walk_reverse(loopback=True):
                    if hasattr(node, 'root_node') and node.root_node:
                        this.root_node = node.root_node
                        break
            assert this.root_node, f'Unable to set root_node for {this}.'
        return func(*args, **kwargs)
    return wrapper


def dispatch_on_initialize(func):
    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        this = args[0]
        if this.is_event_type('on_initialize'):
            this.dispatch('on_initialize')
        return out
    return wrapper


class Node(Widget):

    visible = BooleanProperty(True)

    def _set_ng(self, val): self._neutral_groups = set(val)

    def _get_ng(self): return self._neutral_groups

    # Nodes within this group won't be checked in collisions.
    neutral_groups = AliasProperty(_get_ng, _set_ng)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_body_entered')
        self.register_event_type('on_node_add')
        self.register_event_type('on_node_remove')
        self.register_event_type('on_initialize')
        self.bind(
            visible=self._handle_visible,
        )
        self._neutral_groups = set()

        self.root_node = None  # Reference to the Root Widget

    # Custom events
    def on_initialize(self): pass

    def on_body_entered(self, other): pass

    def on_node_add(self, node): pass

    def on_node_remove(self, node): pass

    # Handlers
    def _handle_visible(self, this, value):
        # self.size_hint_x = 1 if value else 0
        self.opacity = 1 if self.visible else 0
        self.disabled = not self.visible

    def on_kv_post(self, base_widget):
        self.root_node = base_widget
        self.initialize()

    @dispatch_on_initialize
    @ensure_root_node
    def initialize(self):
        return

    def add_widget(self, node, **kwargs):
        super().add_widget(node, **kwargs)
        if hasattr(node, 'initialize'):
            node.initialize()
        if self.is_event_type('on_node_add'):
            self.dispatch('on_node_add', node)

    def remove_widget(self, node):
        if self.is_event_type('on_node_remove'):
            self.dispatch('on_node_remove', node)
        super().remove_widget(node)

    def clear_widgets(self, children=None):
        if self.is_event_type('on_node_remove'):
            _children = children or self.children
            for node in _children:
                self.dispatch('on_node_remove', node)
        super().clear_widgets(children)
