#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Converts a directory of files into a Git repository based on the last
# modified data.
# Copyright (C) 2014  Mark Lee
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, print_function

try:
    import argcomplete
except ImportError:
    argcomplete = None
import argparse
from datetime import datetime
from dateutil.tz import gettz
from dulwich.repo import Repo
from itertools import groupby
import os
import sys


def td_total_secs(td):
    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) *
                10**6) / 10**6


def parse_args(prog, args):
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('directory', metavar='DIR',
                        help='The directory to convert')
    parser.add_argument('committer', metavar='COMMITTER_NAME',
                        help='The name of the git committer')
    parser.add_argument('committer_email', metavar='COMMITTER_EMAIL',
                        help='The email address of the git committer')
    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser.parse_args(args)


def main(argv):
    args = parse_args(argv[0], argv[1:])
    repo = Repo.init(args.directory)
    config = repo.get_config()
    config.set('user', 'name', args.committer)
    config.set('user', 'email', args.committer_email)
    config.write_to_path()
    fdata = []
    tz = gettz()
    for root, dirs, files in os.walk(args.directory):
        for bname in files:
            # TODO handle .gitignore somehow
            if bname.endswith('.pyc') or '/.git' in root:
                continue
            path = os.path.join(root, bname)
            stat = os.lstat(path)
            fdata.append({
                'path': path,
                'lastmod': datetime.fromtimestamp(stat.st_mtime, tz),
                'lastmod_ts': stat.st_mtime,
            })
    kd = lambda f: f['lastmod'].date()
    kdt = lambda f: f['lastmod']
    f_by_lastdate = dict([(k, list(sorted(v, key=kdt)))
                          for k, v in groupby(sorted(fdata, key=kd), kd)])
    for d, metadata in sorted(f_by_lastdate.iteritems()):
        rel_paths = []
        for f in metadata:
            rel_path = f['path'][len(args.directory):]
            rel_paths.append(rel_path)
            repo.stage(rel_path)
        path_list = '\n'.join(['* {}'.format(p) for p in rel_paths])
        author_ts = metadata[-1]['lastmod_ts']
        author_tz = td_total_secs(tz.utcoffset(metadata[-1]['lastmod']))
        repo.do_commit('Auto commit by dir2git', author_timestamp=author_ts,
                       author_timezone=author_tz)
        print(d)
        print(path_list)
        print()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
