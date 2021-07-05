#!/usr/bin/env python3
import sys
import unittest
from collections import OrderedDict
from pathlib import Path

from fileTestSuite.unittest import FileTestSuiteTestCaseMixin

dict = OrderedDict

thisDir = Path(__file__).resolve().absolute().parent
repoRootDir = thisDir.parent

sys.path.insert(0, str(repoRootDir))

from pwexplode import explode


class Tests(unittest.TestCase, FileTestSuiteTestCaseMixin):
    @property
    def fileTestSuiteDir(self) -> Path:
        return thisDir / "testDataset"

    def _testProcessorImpl(self, challFile: Path, respFile: Path, paramsDict=None) -> None:
        self.assertEqual(challFile.read_bytes(), explode(respFile.read_bytes()))


if __name__ == "__main__":
    unittest.main()
