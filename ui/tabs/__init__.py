# ui/tabs/__init__.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from .single import create_single_tab
from .batch import create_batch_tab
from .config import create_config_tab
from .preview import create_preview_tab

__all__ = [
    'create_single_tab',
    'create_batch_tab',
    'create_config_tab',
    'create_preview_tab'
]