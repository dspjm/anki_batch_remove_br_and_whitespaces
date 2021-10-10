# -*- coding: utf-8 -*-
"""
Anki Add-on: Browser Batch Remove Trailing Whitespace and <br>

Adds a menu entry to the card browser that removes trailing whitespace and <br> tags from all fields in all selected notes.

Copyright: Jimmy Pan
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip
from anki.hooks import addHook
from anki import version as anki_version

if anki_version.startswith("2.1"):
    ANKI21 = True
else:
    ANKI21 = False


def RemoveTrailingSpaceAndBr(fields):

	stripped_fields = []
	
	for html in fields:
		while html:
			if html[-4:] == "<br>":
				html = html[:-4]
			elif html[-6:] == "&nbsp;":
				html = html[:-6]
			elif html[len(html)-1] == " ":
				html = html.rstrip()
			else:
				break
		stripped_fields.append(html)

	return stripped_fields

def setupMenu(browser):
    """
    Add the button to the browser menu "edit".
    """
    a = browser.form.menuEdit.addAction('Batch Remove Trailing Whitespaces and <br>')
    # a.setShortcut(QKeySequence(""))
    a.triggered.connect(lambda _, b=browser: onClearTrailing(b))


def onClearTrailing(browser):
    """

    Parameters
    ----------
    browser : Browser
        the anki browser from which the function is called
    """

    nids = browser.selectedNotes()
    if not nids:
        tooltip(_("No cards selected."), period=2000)
        return

    mw.checkpoint("Batch Remove Trailing Whitespaces and <br>")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        note.fields = RemoveTrailingSpaceAndBr(note.fields)
        note.flush()
    mw.progress.finish()
    mw.reset()

# Hooks

addHook("browser.setupMenus", setupMenu)