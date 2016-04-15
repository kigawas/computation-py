from __future__ import print_function, unicode_literals


class State(object):
    def __repr__(self):
        return 'State<{:}>'.format(str(id(self))[-3:])
