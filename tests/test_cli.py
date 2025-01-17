"""Black box integration tests for the command line."""

import subprocess
from subprocess import PIPE


def test1():
    command = "python cli.py --otsu data/IBIS_Case1_V06_t1w_RAI.nrrd"
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    assert proc.stdout.read().rstrip() == b"Calculated Circumference: 433.436 millimeters (mm)"


def test2():
    command = "python cli.py --x=16 --y=2 --z=22 --slice=96 --otsu data/IBIS_Case1_V06_t1w_RAI.nrrd"
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    assert proc.stdout.read().rstrip() == b"Calculated Circumference: 421.511 millimeters (mm)"


def test3():
    command = "python cli.py --slice=69 --lower=0.0 --upper=200.0 data/BCP_Dataset_2month_T1w.nrrd"
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    assert proc.stdout.read().rstrip() == b"Calculated Circumference: 390.444 millimeters (mm)"


def test4():
    command = "python cli.py --otsu data/IBIS_Dataset_NotAligned_6month_T1w.nrrd"
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    assert proc.stdout.read().rstrip() == b"Calculated Circumference: 425.13 millimeters (mm)"


def test5():
    command = "python cli.py --conductance=1.0 --iterations=20 --step=0.05 --otsu data/MicroBiome_1month_T1w.nii.gz"
    proc = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    assert proc.stdout.read().rstrip() == b"Calculated Circumference: 365.712 millimeters (mm)"
