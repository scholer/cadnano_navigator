
= Installation =

To install cadnano_navigator as a plugin, you generally have three options:

1) Download the files and put them in <cadnano-dir>/plugins. This should be done
so that you have a file in: <cadnano-dir>/plugins/cadnano_navigator/__init__.py

2) Download the files as a zip file, change the name of the zip file to .cnp, 
open cadnano preferences -> plugins, click "browse" and select the .cnp file.

3) Clone the git repository to a folder cadnano_navigator, and put that folder in <cadnano-dir>/plugins.

4) Clone the git repository and make *A SYMLINK* to that folder in the <cadnano-dir>/plugins folder.


Pros and cons:
Option 1 and 2 are good for casual users, while option 3 and 4 are better for developers who might want to make changes to the cadnano_navigator code.

Option 3 is good if your <cadnano-dir> is NOT a git repository (if it is, then you will end up with nested git repositories, which can be a mess...)

Option 4 is good if your cadnano is a git repository (cloned from e.g. github).

If you are on windows, please note that due to a bug in python 2.6
which is used by Maya2012, modules in symlink folders cannot be imported.
Thus, if you are on windows and you want to use cadnano from Maya,
you should not use option 4.
Specifically: The old c-code imp module (defined in Python/import.c) has
issues with windows symlinks.




== Regarding the "windows symlink bug on python 2.6" ==
Tested:
* Appending '.py' to the symlink name (suggested in websocket thread) --> DIDN'T WORK.
* Making the symlink inside the plugins folder absolute and NOT RELATIVE --> DIDN'T WORK.

Additional notes:
* importlib not available in python2.6...
* The python 2.6 imp module was renamed to _imp on Apr 15 2012 by Brett Cannon.
* The old _imp/imp module was found in Python/import.c, see http://hg.python.org/cpython/file/d777f854a66e/Python/import.c
