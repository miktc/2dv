# Unit test datavisualizer.py

import csv
from datavisualizer import reset
from datavisualizer import collect_filename
from datavisualizer import add
from datavisualizer import rm
from datavisualizer import edit
import pytest


# The reset will return none
def test_confirm_reset():
    assert reset() == None


# Input filename
def test_collect_filename():
    assert collect_filename() == "test.csv"
    assert collect_filename() == "test.txt"


# Test the reader with a test file
def test_load():
    # Writes a test file data without headers
    with open("testfile.csv","w",newline="\n") as file:
        writer = csv.writer(file)
        writer.writerows(([1,2],[2,3]))

    # Reads the test file data without headers
    with open("testfile.csv","r",newline="\n") as file:
        reader = csv.reader(file)
        returned_row = [row for row in reader]
        assert returned_row == [["1","2"],["2","3"]]


# Add ordered pairs
def test_add_int_positive():
    assert add() == (1,1)
    assert add() == (2,2)
    assert add() == (3,3)

def test_add_flt_positive():
    assert add() == (10.5,10.5)
    assert add() == (20.5,20.5)
    assert add() == (10,10.5)
    assert add() == (20.5,20)
    
def test_add_int_negative():
    assert add() == (-1,-1)
    assert add() == (-2,-2)
    assert add() == (-3,-3)

def test_add_flt_negative():
    assert add() == (-10.5,-10.5)
    assert add() == (-20.5,-20.5)
    assert add() == (-10,-10.5)
    assert add() == (-20.5,-20)


# Edit integer
def test_edit_xint_positive():
    # Edit added (1,1) to (100,1)
    assert edit() == (100,1)
    # Edit added (2,2) to (200,2)
    assert edit() == (200,2)
    
def test_edit_yint_positive():
    # Edit (100,1) to (100,100)
    assert edit() == (100,100)
    # Edit (200,2) to (200,200)
    assert edit() == (200,200)

def test_edit_xint_negative():
    # Edit (100,100) to (-100,100)
    assert edit() == (-100,100)
    # Edit (200,200) to (-200,200)
    assert edit() == (-200,200)

def test_edit_yint_negative():
    # Edit (-100,100) to (-100,-100)
    assert edit() == (-100,-100)
    # Edit (-200,200) to (-200,-200)
    assert edit() == (-200,-200)

# Edit float
def test_edit_xflt_positive():
    # Edit added (10.5,10.5) to (10.1,10.5)
    assert edit() == (10.1,10.5)
    # Edit added (20.5,20.5) to (20.1,20.5)
    assert edit() == (20.1,20.5)

def test_edit_yflt_positive():
    # Edit (10.1,10.5) to (10.1,10.1)
    assert edit() == (10.1,10.1)
    # Edit (20.1,20.5) to (20.1,20.1)
    assert edit() == (20.1,20.1)

def test_edit_xflt_negative():
    # Edit (10.1,10.1) to (-10.1,10.1)
    assert edit() == (-10.1,10.1)
    # Edit (20.1,20.1) to (-20.1,20.1)
    assert edit() == (-20.1,20.1)

def test_edit_yflt_negative():
    # Edit (-10.1,10.1) to (-10.1,-10.1)
    assert edit() == (-10.1,-10.1)
    # Edit (-20.1,20.1) to (-20.1,-20.1)
    assert edit() == (-20.1,-20.1)


# Remove edited ordered pairs
def test_rm_edits():
    assert rm() == (-100,-100)
    assert rm() == (-200,-200)
    assert rm() == (-10.1,-10.1)
    assert rm() == (-20.1,-20.1)

# Remove positive ordered pairs
def test_rm_positive():
    assert rm() == (3,3)
    assert rm() == (10,10.5)
    assert rm() == (20.5,20)

# Remove negative ordered pairs
def test_rm_negative():
    assert rm() == (-1,-1)
    assert rm() == (-2,-2)
    assert rm() == (-3,-3)
    assert rm() == (-10.5,-10.5)
    assert rm() == (-20.5,-20.5)
    assert rm() == (-10,-10.5)
    assert rm() == (-20.5,-20)


if __name__ == "__main__":
    pytest.main(args=["-s"])