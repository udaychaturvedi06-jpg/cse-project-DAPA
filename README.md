
# DAPA (Dynamic Academic Performance/Planner Assistant)

Overview
DAPA is my small academic assistant project where I built a simple tool that helps students calculate their course marks, predict CGPA, and plan their study schedule.
I made this mainly to solve my own confusion about how marks actually add up, and also to help classmates who struggle with grade prediction.

Features

Add and update courses

Enter assignment, quiz, presentation, attendance, mid & final marks

Automatic attendance-to-marks conversion

CGPA calculator

“What-If” mode (try hypothetical marks and see new CGPA)
all courses analysis summary

Study hour planner based on difficulty + credits + performance

Export records (JSON/CSV)

Stores all data in a simple, easy to understand structure

Tech Used

Python 3

Basic file handling (JSON)

Clean modular architecture (data_manager, planner, visualizer, main)

No external heavy libraries needed

Requirements

Make sure you have:

Python 3 installed

A folder named DAPA

All .py files (main.py, planner.py, data_manager.py, visualizer.py) inside that folder

No special dependencies required everything runs with standard Python

How to Run It on vs code
Step 1

Create a folder named DAPA on your computer.
Paste all .py files inside it.

Step 2

Open VS Code → Open the folder DAPA

Step 3

Open the terminal and run:

python main.py

Step 4

The CLI menu will appear. Now you can:

Add courses

Enter marks

Generate CGPA

Try what-if analysis

Export summary

How to Run DAPA on Google Colab

Create a new Google Colab notebook.

Create a folder named "DAPA" inside Colab by running:

!mkdir DAPA

In separate code cells, paste the contents of:
data_manager.py
planner.py
visualizer.py
main.py
using "%writefile" to save them. Example:

%%writefile DAPA/data_manager.py
 paste code here

After saving all files, move into the folder:

%cd DAPA

Run the main program:

!python main.py

The menu will appear inside the Colab output panel.
Type your inputs interactively to operate the system.
