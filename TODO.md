TODO
====

A) Finish writing initial RPM spec file specification

B) __DONE__ Start thinking about how to handle the autoloader

C) Get needed dependencies for RoundCube Mail - I believe that endroid/qr-code
   dependency is an excellent example where the local branch will be needed to
   have an older version than stable branch.

D) Get working install of RoundCube

E) Get working install of three common RoundCube plugins

F) Get other maintainers interested

G) Start working on version database thing to alert system administrators when
   they are using version that needs a security patch. Probably should be done
   in Python. Must work in Python 2.7.5 (what ships in RHEL 7) and should work
   in Python3 as well. Probably should work in Python that RHEL 6 ships.
