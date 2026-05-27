"""When steps for dsl_cli query features."""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

from behave import when

from dsl_cli.orchestrator import run_query


@contextmanager
def _chdir(target: Path):
    prev = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(prev)


@when('dsl_cli query runs with handlers "{handlers}" against the last file')
def step_query_last_file(context, handlers: str):
    handler_list = [item.strip() for item in handlers.split(",") if item.strip()]
    rel = context.last_file_path.relative_to(context.tmp_root)
    with _chdir(context.tmp_root):
        context.query_matches = run_query([rel], handler_list)


@when(
    'dsl_cli query runs with handlers "{handlers}" against files aliased "{a}" and "{b}"'
)
def step_query_two_files(context, handlers: str, a: str, b: str):
    handler_list = [item.strip() for item in handlers.split(",") if item.strip()]
    paths = [context.files[a].relative_to(context.tmp_root), context.files[b].relative_to(context.tmp_root)]
    with _chdir(context.tmp_root):
        context.query_matches = run_query(paths, handler_list)


@when(
    'dsl_cli query runs with handlers "{handlers}" and source-scope "{scope}" '
    'against regular file alias "{regular}" and shared file alias "{shared}"'
)
def step_query_with_scope(context, handlers: str, scope: str, regular: str, shared: str):
    handler_list = [item.strip() for item in handlers.split(",") if item.strip()]
    regular_path = context.files[regular].relative_to(context.tmp_root)
    shared_path = context.files[shared].relative_to(context.tmp_root)
    with _chdir(context.tmp_root):
        context.query_matches = run_query(
            [regular_path],
            handler_list,
            shared_dsl_path=shared_path,
            source_scope=scope,
        )


@when('dsl_cli query runs with handler "{handler}" and source-scope "shared" against shared alias "{shared}"')
def step_query_shared_only(context, handler: str, shared: str):
    shared_path = context.files[shared].relative_to(context.tmp_root)
    with _chdir(context.tmp_root):
        context.query_matches = run_query(
            [],
            [handler],
            shared_dsl_path=shared_path,
            source_scope="shared",
        )
