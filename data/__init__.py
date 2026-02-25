# data/__init__.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from .error_messages import (
    ERROR_MESSAGES,
    SHORT_ERROR_CODES,
    get_random_error,
    get_random_short_code,
    get_random_bios_error,
    format_error_with_hex,
    format_error_with_code,
    format_stack_trace
)

__all__ = [
    'ERROR_MESSAGES',
    'SHORT_ERROR_CODES',
    'get_random_error',
    'get_random_short_code',
    'get_random_bios_error',
    'format_error_with_hex',
    'format_error_with_code',
    'format_stack_trace'
]