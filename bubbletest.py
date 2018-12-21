import random
import sys
import copy
from importlib import util as importutil
from prettytable import PrettyTable

spec = importutil.spec_from_file_location("studenttest", sys.argv[1])
studenttest = importutil.module_from_spec(spec)
spec.loader.exec_module(studenttest)

class TestSection:
    def __init__(self, long, short):
        self.long = long #A longform description of the section and what it tests (to put at start of tests)
        self.short = short #A shortform description of the section (to put in table)
        self.score = 0 #The number of points awarded after testing
        self.total = 0 #The number of points that were available for awarding
    
    def test_equal(self, correctfunction, testfunction, score, *args, **kwargs):
        '''
        Tests if two functions give equal results. Takes as an input:
            correctfunction - a function that is known to be working
            testfunction - a function that you want to tests
            score - how many points should be awarded should the testfunction output match the correctfunction output

        All arguments placed after these three parameters, including kwargs, are passed on as the inputs to the two functions
        '''
        print("  Input:", end=' ')
        print(args, end = " ")
        print(kwargs, end = " ")

        print("  Expected:", end=" ")
        correct = correctfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))
        print(correct)

        print("  Output:",  end=" ")
        output = testfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))
        print(output)

        if correct == output:
            print("  Correct!")
            self.score += score
        else:
            print("  Incorrect!")

        self.total += score

    def end(self):
        print("Section total: {0}/{1}".format(self.score, self.total))

class TestProgram:
    def __init__(self):
        self.currentSection = None
        self.sections = []
    
    def begin_section(self, newsection):
        if not self.currentSection is None:
            raise Exception("Already working on new section")
        self.currentSection = newsection
        print(self.currentSection.long)
    
    def end_section(self):
        self.currentSection.end()
        self.sections.append(self.currentSection)
        self.currentSection = None
    
    def end(self):
        score = 0
        total = 0
        table = PrettyTable(["Section", "Score"])
        for section in self.sections:
            table.add_row([section.short, "{0}/{1}".format(section.score, section.total)])
            score += section.score
            total += section.total
        print("Results:")
        print(table)
        print("Score: {0}/{1} - {2}%".format(score, total, int(round(score*100.0/total, 0))))

def correctBubble(arrayin):
    arrayin.sort()
    return arrayin

def main():
    tester = TestProgram()

    tester.begin_section(TestSection("Ensure that the function handles empty arrays", "(boundary) empty arrays"))
    tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, [])
    tester.end_section()

    tester.begin_section(TestSection("Ensure the function handles arrays of size 1", "(boundary) size 1 array"))
    tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, [2])
    tester.end_section()

    tester.begin_section(TestSection("Checking if function accepts normal lists", "(normal) unsorted arrays"))
    for _ in range(14):
        testList = []
        for _ in range(random.randint(10, 50)):
            testList.append(random.randint(-100, 100))
        tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, testList)
    tester.end_section()

    tester.end()


if __name__ == "__main__":
    main()
