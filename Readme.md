# Automatic tester.

This is a prototype of an automatic tester to be used to mark student's work, live during lessons. When you start `watchdog.py` does the following things:
* Scans a folder for entries
* If it finds one, an entry, it does the following:
  * Run the configured python test program, with the path to the file to be tested as an argument
  * Put the output from that program in a similarly-named html file
  * Scan the output for the score, and then if it is there print it to output (could be implemented to store in database)
  * Move the program that has been tested into a secure store