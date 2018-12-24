# Automatic tester.

This is a prototype of an automatic tester to be used to mark student's work, live during lessons. When you start `watchdog.py` does the following things:
* Scans a folder for entries
* If it finds one, an entry, it does the following:
  * Run the configured python test program, with the path to the file to be tested as an argument
  * Put the output from that program in a similarly-named html file
  * Scan the output for the score, and then if it is there print it to output (could be implemented to store in database)
  * Move the program that has been tested into a secure store

In addition to the `watchdog.py` file, there is an additional `tester.py` file which is useful for generating the html and score as said before. This contains classes for documents, sections and tests. The document encapsulates the entire test, and contains the output document. This then contains an array of sections, which are different areas of the tests being tested. Inside that, there are separaye groups of tests. This all contains all the tests. These were built to be relatively extensible, and you can easily place your own custom module inside this, as long as it has the necessary properties.

Todo:
* Better exception handling for when the watchdog, tester and the given functions fail.
* Output scores to secure database