#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Mark Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flake8.engine import get_style_guide
from flake8.main import print_report
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    # flake8
    flake8 = get_style_guide(exclude=['.tox', 'build'])
    report = flake8.check_files([BASE_DIR])

    # TODO integration test creating a directory to be git-ified
    return print_report(report, flake8)

if __name__ == '__main__':
    sys.exit(main())
