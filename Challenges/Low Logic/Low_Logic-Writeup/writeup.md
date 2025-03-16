# HTB Write-Up: Low Logic

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Reconnaissance](#reconnaissance)
3. [Exploitation](#exploitation)
4. [Post-Exploitation](#post-exploitation)
5. [Privilege Escalation](#privilege-escalation)
6. [Answer](#answer)
7. [Conclusion](#conclusion)

---

## Challenge Overview

- **Name**: Low Logic
- **Category**: Hardware
- **Difficulty**: Very Easy
- **Description**: I have this simple chip, I want you to understand how it's works and then give me the output.
- **Created By**: 0xSn4k3000
- **Date**: 3/15/2025

## Setup

We will be using `python` to script our solution, so ensure that you have Python3 installed on your machince and properly referenced in your PATH. I prefer using venv so I have added some steps below on how to get the solution running and working.

1. Create the virtual environment with python venv

```bash
# On Windows
python -m venv env

# On macOS/Linux
python3 -m venv env
```

2. Activate the virtual environment

```bash
# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate
```

3. Install `solution.py` Dependencies

```bash
pip install -r requirements.txt
```

4. Run `solution.py`

```bash
# With the virtual environment activated
python solve_lowlogic.py
```

5. Decative the Virtual Environment

```bash
# On Windows/macOS/Linux with venv
deactivate

# On Windows/macOS/Linux with conda
conda deactivate
```

## Methodology

### Prior Knowledge

After working through this challenge I would say that while it is labeled as 'very easy', that is given a fundamental understanding of Logic Gates and Circuit Analyis, How you can translate Circuits to Logical Functions and then how those translate relate to Boolean Algebra when paired with the input.

Given that base of understanding I would say that a good grasp on programming languages like Python to parse the input would allow a user to quickly solve this challenge.

### Initial Analysis

After unzipping `Low Logic.zip` we see that the challenege contains two files `chip.jpg` and `input.csv`. This is one of my first hardware solutions so I spent a lot of time searching what type of circuit was described in `chip.jpg`. This caused me refreshen my fundamental understanding of CMOS Circuits and Electrical Engineering.

[TODO: add basic approach to the problem and solution and high-level what solution should be doing]

## Conclusion

`HTB{4_G00d_Cm05_3x4mpl3}`
