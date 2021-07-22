#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pwexplode.py - implementation of the PKWARE Data Compression Library 
# format (imploding) for byte streams
# Copyright (C) 2021 by Sven Kochmann

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the  Free Software Foundation,  either version 3  of the License, or
# (at your option) any later version.

# This program  is distributed  in the hope  that it will  be  useful,
# but  WITHOUT  ANY  WARRANTY;  without even  the implied warranty  of
# MERCHANTABILITY  or  FITNESS  FOR  A  PARTICULAR  PURPOSE.  See  the
# GNU General Public License for more details.

# You  should  have  received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This  script  implements  the  test  suite  based  on  the  testdata 
# collection  prepared  by  KOLANICH,  see:
# https://github.com/implode-compression-impls/implode_test_files

import json
from pathlib import Path
import sys
import unittest

# Remove  tracebacks unless "traceback" is given  in script arguments.
# Need to make sure that "traceback" gets removed from arguments since
# unittest is parsing it.
if not "traceback" in sys.argv:
    __unittest = True
else:
    sys.argv.remove("traceback")
    
# Small  hack  to make  sure that  the main module (pwexplode)  can be 
# imported despite the fact that it is in the parent directory
parentDir = Path(__file__).resolve().absolute().parent.parent
sys.path.insert(0, str(parentDir))
import pwexplode

# In  the  following  we  want  to  generate  ONE  test  case per file 
# comparison. I  found  subtests not fully  suitable  (weird counting,
# etc.). 

# Generate a list with the pairs of files (incl. relative path).  This
# is according to the fileTestSuite specs (since the data set uses it)
# and can be found at: https://github.com/fileTestSuite/fileTestSuite
subpath = "testDataset/"
p = Path(subpath)

list_files = []

def removeMetaFiles(filelist):
    return [file for file in filelist if not file.name in ["License.md", "meta.ftsmeta", "meta.json", "ReadMe.txt", "ReadMe.md"]]

for file in p.rglob("*"):
    if file.is_dir():
        meta = list(file.glob("meta.json"))

        if len(meta) == 1:
            metadata = json.load(meta[0].open())
            print("Parsing", file.name + "/" + meta[0].name, "...")

            # Since sorted, same indices should point to the same
            # pair of files
            rawFiles = removeMetaFiles(sorted(list(file.glob("*" + metadata["rawExt"]))))
            decFiles = removeMetaFiles(sorted(list(file.glob("*" + metadata["processedExt"]))))

            # Hack: remove dec files from raw files (there is the case of no extension given
            # for rawExt of the unshield-dataset. Not optimal. (Also in this case the original
            # dataset has processedExt and rawExt exchanged; as of 2021-07-22)
            rawFiles = [file for file in rawFiles if not file in decFiles]

            if len(rawFiles) == len(decFiles):
                for i in range(len(rawFiles)):
                    basename = rawFiles[i].name[:len(rawFiles[i].name) - len(metadata["rawExt"])]
                    list_files.append({"basename": basename, "imploded": str(decFiles[i]), "exploded": str(rawFiles[i])})                    
                    print("\tAdded %s[%s, %s]." 
                            % (basename, metadata["rawExt"], metadata["processedExt"]))
            else:
                print("There are %d raw files but %d decoded files. That does not fit." 
                        % (len(rawFiles), len(decFiles)))

print("")

# Define a basic test case class and comparison function (will act as "test..." method)
class TestSuperCase(unittest.TestCase):
    pass

def test_generator(imploded, exploded):
    def test(self):
        imploded_data = b""
        exploded_data = b""

        with open(imploded, "rb") as f:
            imploded_data = f.read()

        with open(exploded, "rb") as f:
            exploded_data = f.read()

        self.assertEqual(pwexplode.explode(imploded_data), exploded_data)
    return test

# Generate the Testcases and add a method each for each entry of the list
for filepair in list_files:
    test_name = 'test_%s' % filepair["imploded"]
    test = test_generator(filepair["imploded"], filepair["exploded"])
    setattr(TestSuperCase, test_name, test)

if __name__ == "__main__":
    unittest.main(verbosity=2)
