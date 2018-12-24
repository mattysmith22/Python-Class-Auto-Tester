import html
import copy
import helpers
import csscompressor
import yattag

with open("style.css", "r") as f:
    cssText = f.read()

class TestSet:
    def __init__(self, long, short, index):
        self.long = long #A longform description of the section and what it tests (to put at start of tests)
        self.short = short #A shortform description of the section (to put in table)
        self.index = index
        self.score = 0 #The number of points awarded after testing
        self.total = 0 #The number of points that were available for awarding
        self._testhtmls = []
    
    def test_equal(self, correctfunction, testfunction, score, *args, **kwargs):
        '''
        Tests if two functions give equal results. Takes as an input:
            correctfunction - a function that is known to be working
            testfunction - a function that you want to tests
            score - how many points should be awarded should the testfunction output match the correctfunction output
        All arguments placed after these three parameters, including kwargs, are passed on as the inputs to the two functions
        '''

        doc, tag, text = yattag.Doc().tagtext()

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

        correct = correctfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))
        output = testfunction(*copy.deepcopy(args), **copy.deepcopy(kwargs))

        with tag("ul"):
            with tag("li"):
                text("Input:")
                with tag("code"):
                    text(programargs)
            with tag("li"):
                text("Expected:")
                with tag("code"):
                    text(str(correct))
            with tag("li"):
                text("Output:")
                with tag("code"):
                    text(str(output))

        if correct == output:
            with tag("p"):
                with tag("font", ("color", "green")):
                    text("Correct!")
            self.score += score
        else:
            with tag("p"):
                with tag("font", ("color", "red")):
                    text("Incorrect!")
        self._testhtmls.append(doc.getvalue())
        self.total += score

    def end(self):
        doc, tag, text = yattag.Doc().tagtext()

        with tag("h3", id=self.index):
            text("({}) {}".format(self.index, self.long))
        
        for i in self._testhtmls:
            doc.asis(i)
        
        with tag("p"):
            with tag("b"):
                text("Summary:")
            text(self.score)
            text("/")
            text(self.total)
        self.htmlout = doc.getvalue()

class TestSection:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.sets = []
        self.score = 0
        self.total = 0
    
    def new_set(self, long, short):
        return TestSet(long, short, "{}.{}".format(self.index, len(self.sets)+1))
    
    def add_set(self, set):
        self.sets.append(set)
    
    def end(self):
        doc, tag, text, line = yattag.Doc().ttl()

        with tag("h2", id=self.index):
            text("({}) {}".format(self.index, self.name))
        with tag("table"):
            with tag("thead"):
                with tag("tr"):
                    line("th", "Test Set")
                    line("th", "Score")
                    line("th", "%")
            count = 1
            for i in self.sets:
                with tag("tr"):
                    with tag("th"):
                        line("a", i.short, href="#{}.{}".format(self.index, count))
                    line("th", str(i.score) + "/" + str(i.total))
                    line("th", int(round(i.score * 100 / i.total, 0)))
                self.score += i.score
                self.total += i.total
                count += 1

        for i in self.sets:
            doc.asis(i.htmlout)
        self.htmlout = doc.getvalue()


class TestDocument:
    def __init__(self, name):
        self.sections = []
        self.name = name
    
    def new_section(self, name):
        return TestSection(name, str(len(self.sections)+1))
    
    def add_section(self, section):
        self.sections.append(section)
    
    def end(self):
        score = 0
        total = 0
        doc, tag, text, line = yattag.Doc().ttl()

        doc.asis("<!DOCTYPE html>")
        with tag("html"):
            with tag("head"):
                with tag("style"):
                    doc.asis(csscompressor.compress(cssText))
            with tag("body"):
                with tag("h1"):
                    text("Test results: {}".format(self.name))
                with tag("table"):
                    with tag("thead"):
                        with tag("tr"):
                            line("th", "Section")
                            line("th", "Score")
                            line("th", "%")
                    count = 1
                    for i in self.sections:
                        with tag("tr"):
                            with tag("th"):
                                line("a", i.name, href="#{}".format(count))
                            line("th", str(i.score) + "/" + str(i.total))
                            line("th", int(round(i.score * 100 / i.total, 0)))
                            score += i.score
                            total += i.total
                        count += 1

                with tag("p"):
                    text("Score: {0}/{1} - {2}%".format(html.escape(str(score)),
                                                        html.escape(str(total)),
                                                        html.escape(str(int(round(score*100.0/total, 0))))))

                doc.stag("br")
                doc.stag("br")

                for i in self.sections:
                    doc.asis(i.htmlout)
        self.htmlout = doc.getvalue()