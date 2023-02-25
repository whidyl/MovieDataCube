import sys
import os
import datetime


def make_base_cuboid(input_dir, output_dir):
    os.mkdir(output_dir + "/BASE_CUBOID")
    chunk_files = [open(f"{output_dir}/BASE_CUBOID/{i}.txt", "w") for i in range(1, 101)]
    ratings_file = open(input_dir + "/ratings.txt", "r")

    for line in ratings_file:
        rating_line_reader = RatingLineReader(line)

        # exclude year 2005 from cube
        if rating_line_reader.year == 2005:
            continue

        chunk_files[rating_line_reader.get_chunk_id()-1].write(rating_line_reader.get_chunk_file_line())

    ratings_file.close()
    for file in chunk_files:
        file.close()


class RatingLineReader:
    def __init__(self, line):
        vals = line.split("::")
        user_id, movie_id = int(vals[0]), int(vals[1])

        self.user_id = user_id
        self.movie_id = movie_id
        self.year = datetime.datetime.fromtimestamp(int(vals[3])).year
        self.rating = float(vals[2])
        self.user_partition = get_partition_of_user_id(user_id)
        self.movie_partition = get_partition_of_movie_id(movie_id)

    def get_chunk_file_line(self) -> str:
        return f"{self.user_id}\t{self.movie_id}\t{self.year}\t{self.rating}\t1\n"

    def get_chunk_id(self) -> int:
        """converts into a chunk_id for 0 to 100 counting up by user first, then movie, then year."""
        return self.user_partition + self.movie_partition*5 + (self.year - 2006)*5*5 + 1


def get_partition_of_user_id(user_id):
    if 0 <= user_id <= 16521:
        return 0
    elif 16524 <= user_id <= 31313:
        return 1
    elif 31317 <= user_id <= 46224:
        return 2
    elif 46225 <= user_id <= 61556:
        return 3
    else:
        return 4


def get_partition_of_movie_id(movie_id):
    if 1 <= movie_id <= 2583:
        return 0
    elif 2584 <= movie_id <= 5094:
        return 1
    elif 5095 <= movie_id <= 7836:
        return 2
    elif 7837 <= movie_id <= 55020:
        return 3
    else:
        return 4


file_in = sys.argv[2]
file_out = sys.argv[4]
make_base_cuboid(file_in, file_out)