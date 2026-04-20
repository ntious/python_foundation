# Troubleshooting

Use this guide when something does not work as expected. Most beginner issues are fixable by slowing down, checking one step, and rerunning cells in order.

## Which Option Should I Use?

| Platform | Best For | Reminder |
| --- | --- | --- |
| Binder | Easiest start with no setup | Work may not persist |
| Google Colab | Saving notebook work in Google Drive | Runtime may reset |
| Replit | Optional short Python practice | Notebook support may vary |

## Common Issues

### Notebook Does Not Run

If a notebook does not run:

1. Make sure you opened the file in Binder, Colab, or another notebook tool.
2. Check that the file name ends in `.ipynb`.
3. Start with the first code cell.
4. Run cells from top to bottom.
5. Wait for each cell to finish before running the next one.
6. Refresh the page if the notebook seems frozen.
7. If it still does not work, try opening the notebook in Colab.

Why this matters: notebooks often depend on earlier cells. Skipping cells can cause later code to fail.

### Code Shows an Error

Errors are normal in programming. An error message is a clue, not a sign that you failed.

When code shows an error:

1. Read the last line of the error message.
2. Look for the cell or line mentioned by the error.
3. Check spelling, quotation marks, parentheses, colons, and indentation.
4. Check whether you ran the previous cells in order.
5. Compare your code with the nearest working example.
6. Change one thing.
7. Run the cell again.

If you ask for help, share the error message and say what you already tried.

### Binder Is Slow or Stuck

Binder can take several minutes the first time it opens a course environment.

If Binder is slow:

1. Wait a few minutes.
2. Keep the browser tab open.
3. Avoid clicking the launch link repeatedly.
4. Refresh once if it appears stuck for a long time.
5. Try again later if Binder reports a temporary problem.
6. Switch to Google Colab if you need to keep working.

Why this happens: Binder is preparing a temporary workspace with Python and the course files.

### Lost Work

Browser-based tools can reset or close sessions. Binder work is temporary, and Colab uploaded files can disappear when the runtime resets.

If you lost work:

1. Check whether you downloaded a copy of the notebook.
2. Check Google Drive if you were using Colab.
3. Reopen the original notebook if needed.
4. Recreate the missing work one step at a time.
5. Save or download your work more often next time.

To reduce the risk:

1. In Binder, download important notebooks before closing the tab.
2. In Colab, save a copy in Google Drive.
3. Keep a copy of any data files your notebook needs.

### Output Is Different from the Example

Different output is not always a problem. Your name, numbers, or data values may be different from the example.

If the output should match:

1. Reread the instruction for the cell.
2. Check whether you used the correct values.
3. Run the previous cells again in order.
4. Look for a small typo or missing line.
5. Make one change at a time.
6. Run the cell again.

Focus on whether the output makes sense for the task.

### File Not Found

This error means the notebook cannot find a file it needs, such as a CSV file from the `data/` folder.

To fix it:

1. Check the file name in the code.
2. Make sure the spelling matches exactly.
3. Check that the file is in the expected folder.
4. If you are using Colab, upload the data file again.
5. Run the cell again after the file is available.

Python file names are exact. `sample_scores.csv` and `Sample_Scores.csv` are different names.

### Nothing Happens

If you run a cell and nothing seems to happen:

1. Look below the cell for output.
2. Check whether the cell is still running.
3. Check whether the code is waiting for input.
4. Add or check a `print()` statement if the task expects visible output.
5. Run the cell again.

Some code stores a value without showing output. That can be normal.

### I Do Not Understand What to Do

If the task feels unclear:

1. Reread the instructions slowly.
2. Run the nearest example cell again.
3. Change one small value and observe the result.
4. Write down what you think the task is asking.
5. Try a small first step.
6. Ask your instructor, course support, or a classmate for help.

You do not need to solve everything at once. Small steps are the normal way to learn programming.

## Before Asking for Help

Before asking for help, try to collect:

1. The platform you are using, such as Binder, Colab, or Replit.
2. The notebook name.
3. The cell or section where the issue happened.
4. The error message, if there is one.
5. One thing you already tried.

This information helps someone help you faster.
