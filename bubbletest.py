import random
import sys
import copy
import html
from importlib import util as importutil

spec = importutil.spec_from_file_location("studenttest", sys.argv[1])
studenttest = importutil.module_from_spec(spec)
spec.loader.exec_module(studenttest)

htmlhead = '''
    <head>
        <style>
        table, th, td {
            border: 1px solid black;
        }
        </style>
    </head>
'''

class TestSectionEquals:
    def __init__(self, long, short):
        self.long = long #A longform description of the section and what it tests (to put at start of tests)
        self.short = short #A shortform description of the section (to put in table)
        self.score = 0 #The number of points awarded after testing
        self.total = 0 #The number of points that were available for awarding
        print("<h2>{}</h2>".format(html.escape(self.long)))
        print("<ul>")
    
    def test_equal(self, correctfunction, testfunction, score, *args, **kwargs):
        '''
        Tests if two functions give equal results. Takes as an input:
            correctfunction - a function that is known to be working
            testfunction - a function that you want to tests
            score - how many points should be awarded should the testfunction output match the correctfunction output

        All arguments placed after these three parameters, including kwargs, are passed on as the inputs to the two functions
        '''
        programargs = ""
        for i in args:
            programargs += str(i)
            programargs += ","
        for key, value in kwargs.items():
            programargs += str(key)
            programargs += "="
            programargs += str(value)
            programargs += ","
        programargs = programargs[:-1] #Remove the last 

        print("<li>Input: <code>function({})</code></li>".format(html.escape(programargs)))
        correct = correctfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))
        print("<li>Expected: <code>{}</code></li>".format(html.escape(str(correct))))
        output = testfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))
        print("<li>Output: <code>{}</code></li>".format(html.escape(str(output))))

        if correct == output:
            print("<li><font color=\"green\">Correct!</font></li>")
            self.score += score
        else:
            print("<li><font color=\"red\">Incorrect!</font></li>")

        self.total += score

    def end(self):
        print("</ul>")
        print("<p><b>Summary:</b>{}/{}</p>".format(html.escape(str(self.score)), html.escape(str(self.total))))

class TestProgram:
    def __init__(self):
        self.currentSection = None
        self.sections = []
        print("<html>{}<body>".format(htmlhead))
    
    def begin_section(self, newsection):
        if not self.currentSection is None:
            raise Exception("Already working on new section")
        self.currentSection = newsection
    
    def end_section(self):
        self.currentSection.end()
        self.sections.append(self.currentSection)
        self.currentSection = None
    
    def end(self):
        score = 0
        total = 0
        print("<table>\n<thead>\n<tr><th>Section</th><th>Score</th></tr>\n</thead>\n<tbody>")
        for section in self.sections:
            print("<tr><td>{}</td><td>{}/{}</td></tr>".format(html.escape(str(section.short)), html.escape(str(section.score)), html.escape(str(section.total))))
            score += section.score
            total += section.total
        print("</tbody>\n</table>")
        print("<br /><br /><br />")
        print("<p>Score: {0}/{1} - {2}%</p>".format(html.escape(str(score)), html.escape(str(total)), html.escape(str(int(round(score*100.0/total, 0))))))
        print("</html></body>")

def correctBubble(arrayin):
    arrayin.sort()
    return arrayin

def main():
    tester = TestProgram()

    tester.begin_section(TestSectionEquals("Ensure that the function handles empty arrays", "(boundary) empty arrays"))
    tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, [])
    tester.end_section()

    tester.begin_section(TestSectionEquals("Ensure the function handles arrays of size 1", "(boundary) size 1 array"))
    tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, [2])
    tester.end_section()

    tester.begin_section(TestSectionEquals("Checking if function accepts normal lists", "(normal) unsorted arrays"))
    for _ in range(14):
        testList = []
        for _ in range(random.randint(10, 50)):
            testList.append(random.randint(-100, 100))
        tester.currentSection.test_equal(correctBubble, studenttest.bubble, 2, testList)
    tester.end_section()

    tester.end()


if __name__ == "__main__":
    main()
