"""
Customized reportlab canvas

This file is part of chordlab.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from chordlib import consts

class CanvasAdapter(canvas.Canvas):
    "My convenience adapter for the reportlab canvas."

    def __init__(self, filename, pagesize=A4, margin=50, showfilenames=False,
                 title=None, author=None):
        canvas.Canvas.__init__(self, filename, pagesize=pagesize)

        self.setTitle(title or 'Songbook')

        # reportlab doesn't provide a nicer interface to this (yet)
        self._doc.setAuthor(author or self._guess_author())

        # reportlab doesn't provide a nicer interface to this (yet)
        self._doc.info.producer = 'Chordlab ' + consts.version + '\n' + consts.progurl

        self.pagesize = pagesize
        self.margin = margin
        self.showfilenames = showfilenames

    def _guess_author(self):
        try:
            import pwd, socket, os
            pw = pwd.getpwuid(os.getuid())
            realname = pw.pw_gecos.split(',')[0]
            mailaddr = os.environ.get('MAILADDR')
            if not mailaddr:
                logname = os.environ.get('LOGNAME') or pw.pw_name
                mailaddr = logname + '@' + socket.gethostname()
            return u'%s <%s>' % (realname, mailaddr)
        except:
            print "WARNING: Could not determine author name"
            return None

    def get_left(self):
        "Get left start of drawable area"
        return self.left

    def get_right(self):
        "Get right end of drawable area"
        return self.right

    def get_top(self):
        "Get top start of drawable area"
        return self.top

    def get_bottom(self):
        "Get top end of drawable area"
        return self.bottom

    def draw_aligned_string(self, align, ypos, text):
        if align == 'left':
            meth = self.drawString
            xpos = self.get_left()
        elif align == 'right':
            meth = self.drawRightString
            xpos = self.get_right()
        elif align == 'center':
            meth = self.drawCentredString
            xpos = (self.get_left() + self.get_right()) / 2
        else:
            raise ValueError('bad align: %s' % align)

        meth(xpos, ypos, text)
