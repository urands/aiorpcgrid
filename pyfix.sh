#!/usr/bin/env bash
echo "Collecting python files..."
PY_FILES=$(git ls-files -- '*.py' ':!:*/migrations/*.py')

echo "Running isort (autoformatter) in place..."
poetry run isort -m 3 -tc -q $PY_FILES

echo "Running black (autoformatter) in place..."
poetry run black -l 79 -S --quiet $PY_FILES

echo "Running flake8 (linter)..."
poetry run flake8 $PY_FILES

echo "Running mypy in place..."
poetry run mypy $PY_FILES


complex_files=$(poetry run radon mi -nc $PY_FILES)

if [ "$complex_files" != "" ]; then
  echo "Please check these files for redundant complexity:"
  echo "$complex_files"
fi
