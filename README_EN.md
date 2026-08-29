
** README_EN is translated from README_CN **

ProfessorSearch

This is a Python lightweight tool built using the open-source project PyAlex (https://github.com/J535D165/pyalex) . After running the program, enter a professor's name to search for and select the corresponding scholar from OpenAlex, then view their academic profile.

1. Features

Search professors by name.

Narrow down professors with identical names by affiliated institution.

Display works count, total citation count, and primary  institution in the candidate list.

Display the selected professor's basic profile: OpenAlex ID, ORCID, total works count, total citations, h-index, i10-index, research topics, and research concepts.

Prompt "Is this the professor you are looking for?"; enter y to finish, or n to return and re-select.

Note: Data completeness in OpenAlex varies across profiles. If institutions, keywords, or concepts are missing, the program will display "Not provided"—this is expected behavior, not an error.

2. Requirements

Windows

Python 3.8 or higher

PyAlex

OpenAlex API key (manual configuration required)

This project was developed and tested under a Python 3.13 environment.

3. Getting Started

3.1 Install PyAlex

Run the following command in PowerShell:

PowerShell
python -m pip install pyalex

3.2 Verify Installation

Run the following command in PowerShell:

PowerShell
python -c "from pyalex import Authors; print('PyAlex installed successfully')"
3.3 Configure OpenAlex API Key

Register or log in for free on the official OpenAlex website.

Create and copy your API key at https://openalex.org/settings/api.

Set your API key at the top of ProfessorSearch.py:

Python
import pyalex
pyalex.config.api_key = "YOUR_API_KEY_HERE"
The tool will only function properly after a valid API key is set.

*Do not upload your API key to GitHub or share it with others.

4. Running the Program

Double-click the ProfessorSearch_CN.py file.

The program will prompt you sequentially for:

Plaintext
Please enter the professor's name (English recommended):
Please enter the professor's  institution (English recommended):
Please enter the index of the professor you want to view:
Is this the professor you are looking for? (y/n):
It is recommended to use English names and institution titles, for example:

Plaintext
Professor's name: Albert Einstein
 institution: Princeton University

5. One-Click Launch (Optional)

You can create a batch file named Run_ProfessorSearch.bat with the following content:

DOS
@echo off
python "C:\path\to\your\ProfessorSearch_CN.py"
echo.
pause
Double-click this .bat file to start the program; press any key after execution to close the window.

6. FAQ

Q: What is OpenAlex?
A: OpenAlex is an open-access bibliographic catalog of scientific papers, authors, and institutions, named after the Library of Alexandria. Operated by OurResearch since January 2022, it currently indexes over 250 million scholarly works.

Q: Is it a system error if it displays "Keywords not provided" or "Concept data not provided"?
A: No. OpenAlex does not guarantee that every profile contains these fields; Research Topics are generally more complete.

Q: Why is an API key required?
A: The API key identifies your OpenAlex account and provides higher rate limits suitable for daily queries. For details, see the PyAlex Documentation.

7. Future Enhancements

View a professor's most cited papers.

Filter a professor's papers by publication year.

Export professor profile data to CSV or Excel.

Build a graphical interface (GUI) with input fields and buttons.

Package into a standalone Windows .exe executable.

8. Current Limitations

For common names, the API may return a large volume of results and miss the target profile. Adding additional filter options could resolve this.

The " institution"  has limited accuracy, primarily due to update delays in the OpenAlex database.

Coverage for domestic Chinese-language journal articles is limited.