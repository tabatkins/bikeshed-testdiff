Testdiff
========

Just a little tool I use to help track test changes when I'm making large changes to Bikeshed.

To use: make sure that `main-unaltered` contains the contents of `bikeshed/tests` on the `main` branch (what you're diffing against), then make sure `bikeshed` is on your test branch, with updated tests. Then run `./test`; the file `diff.txt` will contain the diff results.

The tool does some normalization to the test files to remove noisy differences that are unlikely to matter. You can adjust what's normalized in the `setup.py` file.