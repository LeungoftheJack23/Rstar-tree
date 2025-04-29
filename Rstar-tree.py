# Rstar-tree.py, contains the R*-tree implementation and a test case

from classes.RTree import RTree
import os
import random
import noise
import time

# test
def main():    
    # ask the user for input and check if input is valid or not
    try:
        loadPointFile = input("Load point file name? (Enter the file name if exists, or Enter without any input): ")
        if loadPointFile:
            # check if the point directory exists
            if os.path.exists("points"):
                if not loadPointFile.endswith(".txt"):
                    loadPointFile += ".txt"
                
                try:
                    with open(os.path.join("points", loadPointFile), "r") as f:
                        line = f.readline()
                        points = eval(line)
                        numPoints = len(points)
                        pointMethod = loadPointFile.split("p")[0][:-1]
                        print(f"Loaded {numPoints} {pointMethod} points from {loadPointFile}.")
                except:
                    print(f"Error loading file: {loadPointFile}")
                    return
            else:
                print(f"Directory \"points\" does not exist.")
                return
        else:
            numPoints = int(input("Enter the number of points to generate (Range: 1-10000000): "))
            # expect int number range: [1, 10000000]
            if numPoints <= 0:
                print("Invalid input range: Number of points must be greater than 0.")
                return
            
            pointMethod = int(input("Enter the number of method to generate points [1: Random, 2: Uniform, 3: Similar, 4: Perlin Noise]: "))
            if pointMethod == 1:
                pointMethod = "Random"
            elif pointMethod == 2:
                pointMethod = "Uniform"
            elif pointMethod == 3:
                pointMethod = "Similar"
            elif pointMethod == 4:
                pointMethod = "Perlin Noise"
            else:
                print("Invalid input range: Method must be 1, 2, 3 or 4.")
                return

        maxChildren = int(input("Enter the maximum number of children per node (Range: >=3): "))
        # maxChildren should be greater than 2 or else it is no point to create a R*-tree
        if maxChildren <= 2:
            print("Invalid input range: Maximum number of children must be greater than 2.")
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

        if not loadPointFile:
            repetitions = int(input("Enter the number of times to repeat the test (Range: 1-999): "))
        else:
            repetitions = 1
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
        print(f"\n...Running test {i+1}/{repetitions}: using {method} with {numPoints} {pointMethod} points...")
        # create an R*-tree instance
        rtree = RTree(maxChildren=maxChildren, method=method)
        
        if not loadPointFile:
            # generate amount = numPoints
            # generate points method (all round positions to 2 d.p.)
            if pointMethod == "Random":
                # generate random points (can repeat)
                points = set()
                while len(points) < numPoints:
                    x = round(random.random()*100, 2)
                    y = round(random.random()*100, 2)
                    points.add((x, y))
            elif pointMethod == "Uniform":
                # generate unique random points (no repeats)
                points = set()
                while len(points) < numPoints:
                    x = round(random.uniform(0, 100), 2)
                    y = round(random.uniform(0, 100), 2)
                    points.add((x, y))
            elif pointMethod == "Similar":
                # generate base points for other points later
                basePoints = set()
                while len(basePoints) < pow(numPoints, 0.5):
                    x = round(random.uniform(0, 100), 2)
                    y = round(random.uniform(0, 100), 2)
                    basePoints.add((x, y))

                # apply small random offsets to base points for other points
                points = set(basePoints)
                while len(points) < numPoints:
                    basePoint = random.choice(list(basePoints))
                    offset = round(random.uniform(-0.1, 0.1), 2)
                    simPoint = (round(basePoint[0] + offset, 2), round(basePoint[1] + offset, 2))
                    points.add(simPoint)
            elif pointMethod == "Perlin Noise":
                # generate Perlin Noise points
                points = set()
                while len(points) < numPoints:
                    x = round(random.uniform(0, 100), 2)
                    y = round(random.uniform(0, 100), 2)
                    noise_value = noise.pnoise2(x / 10, y / 10, octaves=1)
                    if noise_value > 0.5:
                        points.add((x, y))

            # convert set to list
            points = list(points)
            
            # only save the points to a file if it is not from the loaded file (Name: Random p100 001.txt, Random p100 002.txt, ...)
            dir = "points"
            # make directory if not exist
            os.makedirs(dir, exist_ok=True)
            # get all point files name
            pointFiles = sorted([f for f in os.listdir(dir) if f.startswith(f"{pointMethod} p{numPoints}") and f.endswith(".txt")])
            if pointFiles:
                lastNum = int(pointFiles[-1][-7:-4])
                nextNum = lastNum + 1
            else:
                nextNum = 1
            fileName = f"{pointMethod} p{numPoints} {nextNum:03d}.txt"

            # write the output to the file
            output = []
            output.append(str(points))
            with open(os.path.join(dir, fileName), "w") as f:
                f.write("\n".join(output))
            print(f"Points file saved to \"{fileName}\"")

        # Measure how long it takes to construct the R*-tree
        startTime = time.time()
        for point in points:
            rtree.insert(point)
        endTime = time.time()

        # save time taken, later get average time taken
        timeList.append(f"{endTime - startTime:.4f}")

        # print the output first, then save to file
        print(f"Time taken to construct the R*-tree: {timeList[-1]} seconds")
        # only show structure in console if amount of points <= 1000
        if len(points) <= 1000:
            print("R*-tree structure:")
            print(rtree.display())

        output = []
        output.append(f"Method: {method}")
        output.append(f"Number of points: {numPoints}")
        output.append(f"Generate points method: {pointMethod}")
        output.append(f"Maximum number of children: {maxChildren}")
        output.append(f"Time taken to construct the R*-tree: {timeList[-1]} seconds\n")
        output.append("R*-tree structure:")
        output.append(rtree.display())

        # save the test file (Name: MBR Area Enlargement p100 c3 001.txt, MBR Area Enlargement p100 c3 002.txt, ...)
        dir = "results"
        # make directory if not exist
        os.makedirs(dir, exist_ok=True)
        # get all test files name
        testFiles = sorted([f for f in os.listdir(dir) if f.startswith(method + f" p{numPoints} c{maxChildren}") and f.endswith(".txt")])
        if testFiles:
            lastNum = int(testFiles[-1][-7:-4])
            nextNum = lastNum + 1
        else:
            nextNum = 1
        fileName = f"{method} p{numPoints} c{maxChildren} {nextNum:03d}.txt"

        # write the output to the file
        with open(os.path.join(dir, fileName), "w") as f:
            f.write("\n".join(output))
        print(f"Test results saved to \"{fileName}\"")

    avgTime = sum([float(t) for t in timeList]) / len(timeList)
    print(f"\nAverage time to construct the R*-tree: {avgTime:.4f} seconds")

if __name__ == "__main__":
    main()
