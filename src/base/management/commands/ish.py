from __future__ import annotations

import os
import shlex
import sys
from pathlib import Path
from subprocess import run
from typing import Any
from webbrowser import open as open_url

import click
from django.core.management import BaseCommand, get_commands, load_command_class
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich.text import Text
from textual import events, on
from textual.app import App, AutopilotCallbackType, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalScroll
from textual.css.query import NoMatches
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Label,
    Static,
    Tree,
    Header,
)
from textual.widgets.tree import TreeNode
from trogon.introspect import ArgumentSchema, CommandSchema, MultiValueParamData, OptionSchema
from trogon.run_command import UserCommandData
from trogon.widgets.about import TextDialog
from trogon.widgets.command_info import CommandInfo
from trogon.widgets.command_tree import CommandTree
from trogon.widgets.form import CommandForm
from trogon.widgets.multiple_choice import NonFocusableVerticalScroll
from textual.widgets import TextArea,Static
import django
import traceback
import importlib
import warnings
from django.apps import apps


from pprint import PrettyPrinter


try:
    # Only for python 2
    from StringIO import StringIO
except ImportError:
    # For python 3
    from io import StringIO



def get_py_version():
    ver = sys.version_info
    return "{0}.{1}.{2}".format(ver.major, ver.minor, ver.micro)

def get_dj_version():
    return django.__version__


DEFAULT_IMPORT = {
    'django.db.models': [
        'Avg',
        'Case',
        'Count',
        'F',
        'Max',
        'Min',
        'Prefetch',
        'Q',
        'Sum',
        'When',
    ],
    'django.conf': [
        'settings',
    ],
    'django.core.cache': [
        'cache',
    ],
    'django.contrib.auth': [
        'get_user_model',
    ],
    'django.utils': [
        'timezone',
    ],
    'django.urls': [
        'reverse'
    ],
}

class Importer(object):

    def __init__(self, import_django=None, import_models=None, extra_imports=None):
        self.import_django = import_django or True
        self.import_models = import_models or True
        self.FROM_DJANGO = DEFAULT_IMPORT
        if extra_imports is not None and isinstance(extra_imports, dict):
            self.FROM_DJANGO.update(extra_imports)

    _mods = None

    def get_modules(self):
        """
        Return list of modules and symbols to import
        """
        if self._mods is None:
            self._mods = {}

            if self.import_django and self.FROM_DJANGO:

                for module_name, symbols in self.FROM_DJANGO.items():
                    try:
                        module = importlib.import_module(module_name)
                    except ImportError as e:
                        warnings.warn(
                            "django_admin_shell - autoimport warning :: {msg}".format(
                                msg=str(e)
                            ),
                            ImportWarning
                        )
                        continue

                    self._mods[module_name] = []
                    for symbol_name in symbols:
                        if hasattr(module, symbol_name):
                            self._mods[module_name].append(symbol_name)
                        else:
                            warnings.warn(
                                "django_admin_shell - autoimport warning :: "
                                "AttributeError module '{mod}' has no attribute '{attr}'".format(
                                    mod=module_name,
                                    attr=symbol_name
                                ),
                                ImportWarning
                            )

            if self.import_models:
                for model_class in apps.get_models():
                    _mod = model_class.__module__
                    classes = self._mods.get(_mod, [])
                    classes.append(model_class.__name__)
                    self._mods[_mod] = classes

        return self._mods

    _scope = None

    def get_scope(self):
        """
        Return map with symbols to module/object
        Like:
        "reverse" -> "django.urls.reverse"
        """
        if self._scope is None:
            self._scope = {}
            for module_name, symbols in self.get_modules().items():
                module = importlib.import_module(module_name)
                for symbol_name in symbols:
                    self._scope[symbol_name] = getattr(
                        module,
                        symbol_name
                    )

        return self._scope

    def clear_scope(self):
        """
        clear the scope.

        Freeing declared variables to be garbage collected.
        """
        self._scope = None

    def __str__(self):
        buf = ""
        for module, symbols in self.get_modules().items():
            if symbols:
                buf += "from {mod} import {symbols}\n".format(
                    mod=module,
                    symbols=", ".join(symbols)
                )
        return buf

class Runner(object):

    def __init__(self):
        self.importer = Importer()

    def run_code(self, code):
        """
        Execute code and return result with status = success|error
        Function manipulate stdout to grab output from exec
        """
        status = "success"
        out = ""
        tmp_stdout = sys.stdout
        buf = StringIO()

        try:
            sys.stdout = buf
            exec(code, None, self.importer.get_scope())
            # exec(code, globals())
        except Exception:
            out = traceback.format_exc()
            status = 'error'
        else:
            out = buf.getvalue()
        finally:
            sys.stdout = tmp_stdout

        result = {
            'code': code,
            'out':  out,
            'status': status,
        }
        return result


class ExtendedTextArea(TextArea):
    """A subclass of TextArea with parenthesis-closing functionality."""

    def _on_key(self, event: events.Key) -> None:
        if event.character == "(":
            self.insert("()")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()

class ShellApp(App):
    CSS_PATH = "ish.tcss"

    input_tarea = ExtendedTextArea("", language="python", theme="dracula")
    output_tarea =  TextArea("# Output", language="python", theme="dracula",classes="text-area")

    runner = Runner()

    BINDINGS = [
        Binding(key="r", action="test", description="Run the query"),
        Binding(key="q", action="quit", description="Quit"),
    ]

    def compose(self) -> ComposeResult:
        self.input_tarea.focus()
        yield HorizontalScroll(
            self.input_tarea,
            self.output_tarea,
        )
        yield Label(f"Python: {get_py_version()}  Django: {get_dj_version()}")
        yield Footer()
    
    def action_test(self) -> None:
        code = self.input_tarea.text
        if len(code) > 0:
            # Because the cli - texualize is running on a loop - has an event loop
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
            os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
            django.setup()

            result = self.runner.run_code(code)
            
            printer = PrettyPrinter()
            formatted = printer.pformat(result["out"])

            self.output_tarea.load_text(formatted)

class Command(BaseCommand):
    help = """Run and inspect Django commands in a text-based user interface (TUI)."""

    def handle(self, *args: Any, **options: Any) -> None:
        app = ShellApp()
        app.run()
