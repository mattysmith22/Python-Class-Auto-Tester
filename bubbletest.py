import random
import sys
import copy
import html
import tester
import os.path
from importlib import util as importutil

spec = importutil.spec_from_file_location("studenttest", sys.argv[1])
studenttest = importutil.module_from_spec(spec)
spec.loader.exec_module(studenttest)


def correctBubble(arrayin):
    arrayin.sort()
    return arrayin

def testBubble(document):
    section = document.new_section("Bubble sort")
    testset = section.new_set("Ensure that the function handles empty arrays", "(boundary) empty arrays")
    testset.test_equal(correctBubble, studenttest.bubble, 2, [])
    testset.end()
    section.add_set(testset)

    testset = section.new_set("Ensure the function handles arrays of size 1", "(boundary) size 1 array")
    testset.test_equal(correctBubble, studenttest.bubble, 2, [2])
    testset.end()
    section.add_set(testset)

    testset = section.new_set("Checking if function accepts normal lists", "(normal) unsorted arrays")
    for _ in range(14):
        testList = []
        for _ in range(random.randint(10, 50)):
            testList.append(random.randint(-100, 100))
        testset.test_equal(correctBubble, studenttest.bubble, 2, testList)
    testset.end()
    section.add_set(testset)
    
    section.end()
    return section

def main():
    document = tester.TestDocument(os.path.basename(sys.argv[1]))
    document.add_section(testBubble(document))
    document.end()
    print(document.htmlout)


if __name__ == "__main__":
    main()
