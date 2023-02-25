import sys
import os

def make_2d_cuboids(input_dir, output_dir):
    os.mkdir(output_dir + "/2D_CUBOIDS")
    os.mkdir(output_dir + "/2D_CUBOIDS/UM_CUBOID")
    os.mkdir(output_dir + "/2D_CUBOIDS/UY_CUBOID")
    os.mkdir(output_dir + "/2D_CUBOIDS/MY_CUBOID")

    uy_chunks = [{} for i in range(1, 5*4 + 1)]
    my_chunks = [{} for i in range(1, 5*4 + 1)]

    for u in range(5):
        for m in range(5):
            um_chunk = {} # memory will be freed after looping through years
            for y in [2006, 2007, 2008, 2009]:
                uy_chunk = uy_chunks[uy_to_chunk_id(u, y)-1]
                my_chunk = my_chunks[my_to_chunk_id(m, y)-1]

                base_chunk_file = open(input_dir + f"/BASE_CUBOID/{umy_to_chunk_id(u, m, y)}.txt")
                for line in base_chunk_file:
                    base_reader = ChunkLineReader(line)
                    aggregate_into_chunk(um_chunk, (base_reader.user_id, base_reader.movie_id), base_reader.rating)
                    aggregate_into_chunk(uy_chunk, (base_reader.user_id, base_reader.year), base_reader.rating)
                    aggregate_into_chunk(my_chunk, (base_reader.movie_id, base_reader.year), base_reader.rating)
                base_chunk_file.close()

                # uy_chunks are finished once all m are aggregated
                if m == 4:
                    write_uy_chunk(uy_chunk, u, y, output_dir)
                    uy_chunks[uy_to_chunk_id(u, y)-1] = None # free from memory

                # my_chunks are finished once all u are aggregated
                if u == 4:
                    write_my_chunk(my_chunk, m, y, output_dir)
                    my_chunks[my_to_chunk_id(m, y)-1] = None # free from memory

            # a um_chunk is finished after each row of years is processed
            write_um_chunk(um_chunk, u, m, output_dir)


def write_um_chunk(um_chunk, u, m, output_dir):
    um_chunk_file = open(f"{output_dir}/2D_CUBOIDS/UM_CUBOID/{um_to_chunk_id(u, m)}.txt", "w")
    um_chunk_file.write("\n".join(
        [f'{user_id}\t{movie_id}\t{rating / count}\t{count}' for (user_id, movie_id), (rating, count) in
         um_chunk.items()]))
    um_chunk_file.close()


def write_my_chunk(my_chunk, m, y, output_dir):
    my_chunk_file = open(f"{output_dir}/2D_CUBOIDS/MY_CUBOID/{my_to_chunk_id(m, y)}.txt", "w")
    my_chunk_file.write(chunk_dict_to_str(my_chunk))
    my_chunk_file.close()


def write_uy_chunk(uy_chunk, u, y, output_dir):
    uy_chunk_file = open(f"{output_dir}/2D_CUBOIDS/UY_CUBOID/{uy_to_chunk_id(u, y)}.txt", "w")
    uy_chunk_file.write(chunk_dict_to_str(uy_chunk))
    uy_chunk_file.close()


def chunk_dict_to_str(chunk):
    return "\n".join(
        [f'{val1}\t{val2}\t{rating / count}\t{count}' for (val1, val2), (rating, count) in
         chunk.items()])


class ChunkLineReader:
    def __init__(self, line):
        line = line.replace("\n", "")
        vals = line.split("\t")

        self.user_id = vals[0]
        self.movie_id = vals[1]
        self.year = vals[2]
        self.rating = float(vals[3])


def umy_to_chunk_id(u, m, y) -> int:
    """converts into a chunk_id for 0 to 100 counting up by user first, then movie, then year."""
    return u + m*5 + (y - 2006)*5*5 + 1


def um_to_chunk_id(u, m) -> int:
    return u + m*5 + 1


def uy_to_chunk_id(u, y) -> int:
    return u + (y - 2006)*5 + 1


def my_to_chunk_id(m, y) -> int:
    return m + (y - 2006)*5 + 1


def aggregate_into_chunk(chunk, key, rating, count=1):
    if key not in chunk:
        chunk[key] = [rating, count]
    else:
        chunk[key][0] += rating
        chunk[key][1] += count


file_in = sys.argv[2]
file_out = sys.argv[4]
make_2d_cuboids(file_in, file_out)