# Steiner-tree-visualiser
Built for IB Extended Essay. Visualises and compares three methods for connecting four cities (A, B, C, D), showing that the Steiner tree produces a shorter total network than simpler alternatives.

<img width="1610" height="811" alt="image" src="https://github.com/user-attachments/assets/2b0fc9f0-e466-49b0-a718-8ec617fd81ce" />

# How to run
## Install dependencies: 
pip install matplotlib numpy shapely scikit-spatial

## Run the Melzak visualiser:
python melzak_algorithm_code.py

When prompted, enter 1 or 2 to choose which Steiner tree topology to compute (there are two valid configurations).

# Melzak Algorithm
Given any four points, the algorithm works by constructing a series of equilateral triangles on the edges of the quadrilateral, then using circle intersections to locate the two optimal junction points that minimise total network length. 

A nice illustration of how geometry from ancient Greece still turns up in modern path-finding problems!
