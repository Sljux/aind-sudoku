# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

This is an AI for solving diagonal Sudoku puzzles written in Python. It uses constraint propagation and search to achieve
this.

Constraint propagation is a method of finding values for a set of variables that satisfy a set of constraints, e.g
digits for boxes in a Sudoku puzzle. Each variable has a defined domain (set of allowed values), e.g. digit from 1 to 9
for a Sudoku box. A solution is a combination of allowed values assigned to variables, that satisfy all of constraints.
Constraint propagation consists of iteratively eliminating possible values for a subset of variables, until a solution 
is found, or it is shown that no solution is possible.

Naked Twins Sudoku exclusion strategy works as follows: If two boxes in a unit have the same two possible values, but 
it is still unknown which one box which value, we can eliminate the two values from all the other boxes in the unit.

![naked twins](https://d17h27t6h515a5.cloudfront.net/topher/2017/January/5877cc63_naked-twins/naked-twins.png)

As shown in the image above, the third row contains two boxes with only two possible values - 2 and 3. It is still not
clear which one should hold 2 and which one should hold 3, but it is certain we can eliminate 2 and 3 from all other
boxes in the third row:

![naked twins eliminated](https://d17h27t6h515a5.cloudfront.net/topher/2017/January/5877cc78_naked-twins-2/naked-twins-2.png)

By implementing this strategy as a constraint, Sudoku solving AI doesn't actually find a definitive value for a
particular box, but it eliminates a lot of possibilities from other boxes. Hence, enforcing the Naked Twins constraint
creates a smaller tree of possible Sudoku solutions, making the search step, and the whole constraint propagation,
faster.

Naked twins constraint is implemented as follows:

```python
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        # Find values of length 2 in a unit which appear more than once
        duplicates = [val for val, count in
                      Counter([values[box] for box in unit if len(values[box]) == 2]).items()
                      if count > 1]

        for dup in duplicates:
            for box in unit:
                # Don't touch the duplicate itself
                if values[box] == dup:
                    continue

                for digit in dup:
                    assign_value(values, box, values[box].replace(digit, ''))

    return values
```

A diagonal Sudoku is an extension of the classical Sudoku puzzle. In addition to standard Sudoku units - rows, columns
and principal squares - diagonal Sudoku requires that values on both diagonals consist only of unique values, i.e. that
digits from 1 to 9 appear only once.

This is implemented by adding diagonals to the list of Sudoku units:

```python
# Diagonal units
main_diag = [a + b for a, b in zip(rows, cols)]
anti_diag = [a + b for a, b in zip(rows, cols[::-1])]
diag_units = [main_diag, anti_diag]
```

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that
contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for
setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in
solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant,
which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command 
`pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.
 You will be prompted for a username and password.  If you login using google or facebook,
 visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip. This is the file that you should
submit to the Udacity reviews system.

