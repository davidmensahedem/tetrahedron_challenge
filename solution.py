# Description: This script reads a file containing a list of points in 3D space and their associated numbers.
# It then finds the smallest valid tetrahedron (a 3D shape with 4 vertices) that can be formed using 4 of the points.
# The sum of the numbers associated with the 4 points must be 100.
# The script then calculates the volume of the tetrahedron and returns the indices of the 4 points that form the smallest valid tetrahedron.

# By:David Mensah
# Role: Software Engineer - FullStack

import itertools
import os

def return_tetrahedron_volume(p1, p2, p3, p4):
    AB = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    AC = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    AD = (p4[0] - p1[0], p4[1] - p1[1], p4[2] - p1[2])

    cross_product_x = AB[1] * AC[2] - AB[2] * AC[1]
    cross_product_y = AB[2] * AC[0] - AB[0] * AC[2]
    cross_product_z = AB[0] * AC[1] - AB[1] * AC[0]

    scalar_triple_product = (
        AD[0] * cross_product_x +
        AD[1] * cross_product_y +
        AD[2] * cross_product_z
    )

    return abs(scalar_triple_product) / 6.0

def return_coordinates_from_file(filename):
    coordinates = []
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
    
    with open(filename, 'r') as points_file:
        for line in points_file:
            try:
                line = line.strip().strip('()')
                x, y, z, n = line.split(',')
                
                if not x or not y or not z or not n:
                    raise ValueError("Invalid input file. Coordinates not valid to be used.")
                
                x,y,z,n = float(x), float(y), float(z), int(n)
                
                if not (isinstance(x, float) and isinstance(y, float) and isinstance(z, float) and isinstance(n, int)):
                    raise ValueError("Coordinate values are not numbers.")
                
                if not (0 <= n <= 100):
                    raise ValueError("The associated number must be from the range of 0 to 100.")
                
                coordinates.append((x, y, z, n))
                
            except ValueError as e:
                raise ValueError(f"Invalid input file. {e}")
            
    return coordinates

def return_smallest_valid_tetrahedron_indices(points):
    best_tetrahedron_indices = None
    min_tetrahedron_volume = float('inf')
    
    for combination in itertools.combinations(enumerate(points), 4):
        indices, coordinates_list = zip(*combination)
        
        sum = 0
        
        for coordinate in coordinates_list:
            sum += coordinate[3]
            
        if sum == 100:
            volume = return_tetrahedron_volume(*coordinates_list)
            if volume < min_tetrahedron_volume:
                min_tetrahedron_volume = volume
                best_tetrahedron_indices = indices
    
    return sorted(best_tetrahedron_indices) if best_tetrahedron_indices else []

small_points = 'data/points_small.txt'
large_points = 'data/points_large.txt'

small_coordinates = return_coordinates_from_file(small_points)
large_coordinates = return_coordinates_from_file(large_points)

small_indices = return_smallest_valid_tetrahedron_indices(small_coordinates)
large_indices = return_smallest_valid_tetrahedron_indices(large_coordinates)

print(f"Smallest valid tetrahedron indices for small points: {small_indices}")
print(f"Smallest valid tetrahedron indices for large points: {large_indices}")