#!/bin/sh

pip install --upgrade pip || exit 1
pip install -e .[dev,test] || exit 1
pip install -e tests/cli/subcommands/example_project || exit 1
pip install -e tests/cli/projects/types_dsl || exit 1
pip install -e tests/cli/projects/data_dsl || exit 1
pip install -e tests/cli/projects/flow_dsl || exit 1
pip install -e tests/cli/projects/flow_codegen || exit 1
