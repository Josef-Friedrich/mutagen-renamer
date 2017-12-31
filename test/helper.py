# -*- coding: utf-8 -*-

"""Helper module for all tests."""

import os
import shutil
import tempfile
import sys
import six
import re
import audiorename

if six.PY2:
    from cStringIO import StringIO
else:
    from io import StringIO


dir_test = os.path.dirname(os.path.abspath(__file__))
dir_cwd = os.getcwd()
path_album = '/t/the album artist/the album_2001/4-02_full.mp3'
path_compilation = '/_compilations/t/the album_2001/4-02_full.mp3'
test_files = os.path.join(dir_test, 'files')


def gen_file_list(files, path, extension='mp3'):
    output = []
    for f in files:
        if extension:
            f = f + '.' + extension
        output.append(os.path.join(path, f))
    return output


def get_meta(path_list):
    return audiorename.meta.Meta(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            *path_list
        ),
        audiorename.args.ArgsDefault()
    )


def has(list, search):
    """Check of a string is in list

    :param list list: A list to search in.
    :param str search: The string to search.
    """
    return any(search in string for string in list)


def is_file(path):
    """Check if file exists

    :param list path: Path of the file as a list
    """
    return os.path.isfile(path)


def copy_to_tmp(path_list):
    """
    :param list path_list: A list of path segments.
    """
    orig = os.path.join(os.path.dirname(os.path.abspath(__file__)), *path_list)

    tmp = os.path.join(tempfile.mkdtemp(), os.path.basename(orig))
    shutil.copyfile(orig, tmp)
    return tmp


class Capturing(list):

    def __init__(self, channel='out'):
        self.channel = channel

    def __enter__(self):
        if self.channel == 'out':
            self._pipe = sys.stdout
            sys.stdout = self._stringio = StringIO()
        elif self.channel == 'err':
            self._pipe = sys.stderr
            sys.stderr = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        if self.channel == 'out':
            sys.stdout = self._pipe
        elif self.channel == 'err':
            sys.stderr = self._pipe


def dry_run(options):
    with Capturing() as output:
        audiorename.execute([
            '--target', '/',
            '--dry-run',
            '--shell-friendly'
        ] + options)

    output = re.sub(r'.*-> ', '', output[1])
    return re.sub(r'\x1b\[[\d;]*m', '', output)
