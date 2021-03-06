from RadixTree import *
import random
import numpy as np

import unittest


class RadixTreeTest(unittest.TestCase):
    def test_init_1(self):
        tree = RadixTree(["mother","mot","fuse","fusing", "mother", "mot"])
        self.assertEqual(set(tree), {"mother","mot","fuse","fusing"})

    def test_LenAttr_1(self):
        tree = RadixTree([""])
        self.assertEqual(len(tree), 0)

    def test_LenAttr_2(self):
        tree = RadixTree(["mom", "mom", "monk", "tree", "three"])
        self.assertEqual(len(tree), 4)

    def test_LenAttr_3(self):
        tree = RadixTree(["mom", "mother", "monk", "monk", "tree", "three", "father",
                          "feather", "", "nothing", "123", "1223", "123"])
        print(set(tree))
        self.assertEqual(len(tree), 10)

    #################

    def test_ContainsAttr_1(self):
        tree = RadixTree(["mom", "mother", "monk", "tree", "three", "father",
                          "feather", "", "nothing", "123", "1223", "123"])
        self.assertEqual("mom" in tree, True)

    def test_ContainsAttr_2(self):
        tree = RadixTree(["mom", "mother", "monk", "tree", "three", "father",
                          "feather", "", "nothing", "123", "1223", "123"])
        self.assertEqual("mothe" in tree, False)

    def test_ContainsAttr_3(self):
        tree = RadixTree(["mom", "mother", "monk", "tree", "three", "father",
                          "feather", "", "nothing", "123", "1223", "123"])
        self.assertEqual("" in tree, False)

    #################

    def test_KidsFunc_1(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(tree.kids("expect"), ["expectation"])

    def test_KidsFunc_2(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree.kids("exp")), {"expel",
                                                 "expense",
                                                 "expensive",
                                                 "expose",
                                                 "exposure",
                                                 "expect",
                                                 "expectation"})

    def test_KidsFunc_3(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree.kids("11")),  {"1123", "113"})

    ###############

    def test_ParentsFunc_1(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree.parents("1233211")), {"1", "123", "123321"})

    def test_ParentsFunc_2(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree.parents("expectation is")), {"expect", "expectation"})

    def test_ParentsFunc_3(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(tree.parents("expel"), [])

    def test_iterate_1(self):
        data = {"excitement", "exercise", "expel", "excellent", "extend", "exorbitant", "expense", "expensive",
                "expose", "exposure", "exude", "exit", "expect", "expectation", "exasperating", "1", "1123", "123",
                "123321", "113"}
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        res = []
        for i in tree:
            res.append(i)
        self.assertEqual(set(res),data)

    def test_StructParentsFunc_1(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree.structural_parents("expe")), {"ex","exp"})

    def test_export_import1(self):
        tree = RadixTree(["excitement", "exercise", "expel", "excellent", "extend",
                          "exorbitant", "expense", "expensive", "expose", "exposure",
                          "exude", "exit", "expect", "expectation", "exasperating",
                          "1", "1123", "123", "123321", "113"])
        self.assertEqual(set(tree),set(RadixTree(tree.export(),1)))


if __name__ == "__main__":
    unittest.main(verbosity=12)


