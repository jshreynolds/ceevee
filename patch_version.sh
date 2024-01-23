#!/bin/bash

poetry version patch && \
git add pyproject.toml && \
git commit -m "fix: patching version for release" && \
git tag $(poetry version --short) && \
git push && \
git push origin $(poetry version --short)