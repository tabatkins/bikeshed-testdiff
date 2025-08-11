from __future__ import annotations

# This code sets up test folders for diffing, and removes "insignificant" differences
# to make the diff easier to read.
# When running this, start with /main-unaltered containing being a copy
# of /bikeshed/tests from the main branch, and bikeshed having the new
# branch checked out.

# TODO: Make this automatically stash the current bikeshed folder,
# check out the nearest common ancestor of the branch and main,
# then copy over the tests from there itself
# before switching back, unstashing, and setting up the tests.

import os
import re

def run():
    testFolder = os.path.dirname(os.path.realpath(__file__))
    testFolderName = os.path.basename(testFolder)

    for path in findFilePaths(testFolder+"/main-unaltered", ".html"):
        # Read in the unaltered main branch test output from /main-unaltered
        # and normalize it.
        mainInput = path
        with open(mainInput, 'r', encoding='utf-8') as fh:
            text = normalizeFile(fh.read())

        # Write it out to /main, for diffing
        mainOutput = path.replace("main-unaltered", "main")
        os.makedirs(os.path.dirname(mainOutput), exist_ok=True)
        with open(mainOutput, 'w', encoding='utf-8') as fh:
            fh.write(text)

        # Read in the same file directly from the bikeshed folder,
        # and normalize it.
        parseInput = path.replace(f"{testFolderName}/main-unaltered", "bikeshed/tests")
        with open(parseInput, 'r', encoding='utf-8') as fh:
            text = normalizeFile(fh.read())

        # Write it out to /modified, for diffing
        parseOutput = path.replace("main-unaltered", "modified")
        os.makedirs(os.path.dirname(parseOutput), exist_ok=True)
        with open(parseOutput, 'w+', encoding='utf-8') as fh:
            fh.write(text)


def findFilePaths(rootFolder, ext):
    paths = []
    for root, _, filenames in os.walk(rootFolder):
        for filename in filenames:
            fullPath = os.path.join(root, filename)
            extension = os.path.splitext(fullPath)[1]
            if extension != ext:
                continue
            paths.append(fullPath)
    return paths

def normalizeFile(text: str) -> None:
    ### These are the generally useful normalizations that should always be on.
    # Remove the dedup digits from ids/links.
    text = re.sub(r"[⓪①②③④⑤⑥⑦⑧⑨]", "", text)
    # Kill the dfnpanel data lines,
    text = removeLine(text, r"\"[^\"]+\": {\"dfnID")
    text = removeLine(text, r"\"[^\"]+\": {\"export")
    text = removeLine(text, r"\"#[^\"]+\": {\"displayText")
    #text = removeLine(text, r"\s*<p></p>")
    
    ### Add any situation-specific normalizations here.
    text = removeLine(text, r"\s*<tbody>")
    text = re.sub(r"xmlns:xlink", "xlink", text)
    text = re.sub(r"\s+</p>", "</p>", text)

    return text

def removeLine(text: str, pattern: str) -> str:
    return re.sub(r"\n" + pattern + r"[^\n]*", "", text)

if __name__ == "__main__":
    run()