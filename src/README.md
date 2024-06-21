Way to run main.py:

1. Move into COMP307AS4 directory on terminal: cd COMP307AS4
2. Move into src directory: cd src
3. Run main.py: python3 main.py

How to run n32-k5.vrp and n80-k10.vrp:
- Have left optimal, nearest neighbor, savings heuristic uncommented.
- Is currently running n32-k5.vrp. To switch to run n80-k10.vrp comment lines 12 and 13 and uncomment lines 15 and 16.

Issues:
- Had issues setting up matplotlib.pyplot with issues coming from line 86 in utility.py.
- Have fixed this by replacing it with line 87. Have tested this on ECS computers and works with line 87.
- If any issues arise look at cm.py file and matlib documentation to fix or use original template code.