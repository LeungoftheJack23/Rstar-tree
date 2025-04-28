# Rstar-tree.py, contains the R*-tree implementation and a test case

from classes.RTree import RTree
import os
import random
import time

# test
def main():    
    # ask the user for input and check if input is valid or not
    try:
        numPoints = int(input("Enter the number of points to generate (Range: 1-10000000): "))
        # expect int number range: [1, 10000000]
        if numPoints <= 0:
            print("Invalid input range: Number of points must be greater than 0.")
            return
        
        maxChildren = int(input("Enter the maximum number of children per node (Range: >=2): "))
        # maxChildren should be greater than 1 or else it is no point to create a R*-tree
        if maxChildren <= 1:
            print("Invalid input range: Maximum number of children must be greater than 1.")
            return

        method = int(input("Enter the number of method to implement [1: MBR Area Enlargement, 2: MBR Margin Enlargement, 3: MBR Overlap Change]: "))
        if method == 1:
            method = "MBR Area Enlargement"
        elif method == 2:
            method = "MBR Margin Enlargement"
        elif method == 3:
            method = "MBR Overlap Change"
        else:
            print("Invalid input range: Method must be 1, 2 or 3.")
            return

        repetitions = int(input("Enter the number of times to repeat the test (Range: 1-999): "))
        if repetitions <= 0:
            print("Invalid input range: Number of repetitions must be greater than 0.")
            return
        elif repetitions > 999:
            print("Invalid input range: Number of repetitions must be less than or equal to 999.")
            return
    except ValueError:
        print("Invalid input type: Please enter a valid integer on points, method and repetitions.")
        return

    timeList = []
    for i in range(repetitions):
        print(f"\n...Running test {i+1}/{repetitions}: using {method} with {numPoints} points...")
        # create an R*-tree instance
        rtree = RTree(maxChildren=maxChildren, method=method)
        
        # generate amount:numPoints unique random points (no repeats) and round positions to 2 d.p.
        points = set()
        while len(points) < numPoints:
            x = round(random.uniform(0, 100), 2)
            y = round(random.uniform(0, 100), 2)
            points.add((x, y))

        # convert set to list
        points = list(points)

        # Measure how long it takes to construct the R*-tree
        start_time = time.time()
        for point in points:
            rtree.insert(point)
        end_time = time.time()

        # save time taken, later get average time taken
        timeList.append(f"{end_time - start_time:.4f}")

        # print the output first, then save to file
        print(f"Time taken to construct the R-tree: {timeList[-1]} seconds")
        # only show structure in console if amount of points <= 1000
        if len(points) <= 1000:
            print("R*-tree structure:")
            print(rtree.display())

        output = []
        output.append(f"Method: {method}")
        output.append(f"Number of points: {numPoints}")
        output.append(f"Maximum number of children: {maxChildren}")
        output.append(f"Time taken to construct the R-tree: {timeList[-1]} seconds\n")
        output.append("R*-tree structure:")
        output.append(rtree.display())

        # save the test file (Name: test001.txt, test002.txt, ...)
        dir = "results"
        # make directory if not exist
        os.makedirs(dir, exist_ok=True)
        # get all test files name
        test_files = sorted([f for f in os.listdir(dir) if f.startswith(method + f" p{numPoints} c{maxChildren}") and f.endswith(".txt")])
        if test_files:
            last_test_number = int(test_files[-1][-7:-4])
            next_test_number = last_test_number + 1
        else:
            next_test_number = 1
        fileName = f"{method} p{numPoints} c{maxChildren} {next_test_number:03d}.txt"

        # write the output to the file
        with open(os.path.join(dir, fileName), "w") as f:
            f.write("\n".join(output))
        print(f"Test results saved to {fileName}")

if __name__ == "__main__":
    main()