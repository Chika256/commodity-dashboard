"""Smoke tests to ensure importability before full implementation."""

import importlib


def test_import_app():
    module = importlib.import_module("app")
    assert hasattr(module, "main")
