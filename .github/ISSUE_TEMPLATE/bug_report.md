---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Version Number**
The exact version you are experiencing this error in.

**Error Report**
Go into the directory of the `msrf.exe` application and look for a folder called `errors`.  This folder will include auto generated error reports to help debug problems. 

These error reports may include personal information, so please read the following:

Error reports will show up in the log window, it will say "Error report generated" with a filename at the end. That is the zipfile that includes the error report for that specific error. 

- Error Information
	- Account data (Same account data used for earning points, this information does not contain any account credentials, only account information like: point count, available promotions, etc.) 
	- Browser screenshot at the time of the error. This may include the account name, and potentially the account email. If you plan on sharing this (such as in a Github issue), you may want to cover any personal information
	- A traceback. This is the exception raised by python. 
	- The HTML page at the time of the error. This helps in determining exactly why an error happened, but this file will have personal information, such as your email address and name. You may not want to include this when sharing this with other people. If you are familiar with HTML structure, you can find and remove that personal information before sharing. 
	- the url that the exception occured on.

You can unzip the error report and hide any personal information before including it in your Github issue. 

Including an error report in your issue will help me solve your problem. Many issues in MSRF are directly related to the microsoft account and changes/variations in Microsoft rewards. The error report targets exactly what the problem is. You are unlikely to get help by creating an issue that says "Its not working" with no additional information.
