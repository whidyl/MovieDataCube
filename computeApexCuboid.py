import sys

def make_apex_cuboid(input_dir):
    sum_rating = 0
    total_count = 0
    for i in range(1, 5):
        y_chunk = open(input_dir + f"/1D_CUBOIDS/Y_CUBOID/{i}.txt")
        for line in y_chunk:
            chunk_reader = ChunkLineReader(line)
            sum_rating += chunk_reader.rating
            total_count += chunk_reader.count
    print(f"avg rating: {sum_rating/4}, total_reviews: {total_count}")


class ChunkLineReader:
    def __init__(self, line):
        line = line.replace("\n", "")
        vals = line.split("\t")

        self.year = vals[0]
        self.rating = float(vals[1])
        self.count = int(vals[2])


file_in = sys.argv[2]
make_apex_cuboid(file_in)