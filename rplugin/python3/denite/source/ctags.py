import typing
import os
import re

from .base import Base
from denite import util

class Source(Base):
    def __init__(self, vim: util.Nvim) -> None:
        super().__init__(vim)
        self.name = 'ctags'
        self.kind = 'file'
        self.vim = vim
        self.is_volatile = True

    def on_init(self, context: util.UserContext) -> None:
        context['__patterns'] = dict(enumerate(context['args']))

    def gather_candidates(self, context: util.UserContext) -> util.Candidates:
        if len(context['args']) == 0:
            return []

        taglist = self.vim.call('taglist', context['args'][0])

        if len(taglist) == 0:
            return []

        return [ self._candidate(i) for i in taglist ]

    def highlight(self) -> None:
        self.vim.command(
                'syntax keyword {0}_searchedWord {1} contained containedin={0}'.format(
                    self.syntax_name, self.context['__patterns'][0] if len(self.context['__patterns']) > 0 else ''))
        self.vim.command('highlight default link {}_searchedWord Function'.format(self.syntax_name))

    def _candidate(self, tag):
        filename = tag['filename']
        path_name = os.path.split(filename)
        line = re.sub('\/\^|\$\/', '', tag['cmd'])

        return {
                'word' : '{}/{}     {}'.format(util.truncate(self.vim, path_name[0], 50), path_name[1], line),
                'abbr' : '{}/{}     {}'.format(util.truncate(self.vim, path_name[0], 50), path_name[1], line),
                'action__path' : filename,
                'action__text' : line,
                'action__pattern' : line
                }

