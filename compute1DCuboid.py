import os
import sys

def make_1d_cuboids(input_dir, output_dir):
    #um_cuboid, my_cuboid, uy_cuboid
    os.mkdir(output_dir + "/1D_CUBOIDS")
    os.mkdir(output_dir + "/1D_CUBOIDS/U_CUBOID")
    os.mkdir(output_dir + "/1D_CUBOIDS/M_CUBOID")
    os.mkdir(output_dir + "/1D_CUBOIDS/Y_CUBOID")

    # UY_CUBOID has the smallest sized cuboid for computing the U_CUBOID
    for u in range(5):
        u_chunk = {}
        for y in [2006, 2007, 2008, 2009]:
            uy_chunk_file = open(input_dir + f"/2D_CUBOIDS/MY_CUBOID/{my_to_chunk_id(u, y)}.txt")
            for line in uy_chunk_file:
                chunk_reader = ChunkLineReader(line)
                aggregate_into_chunk(u_chunk, chunk_reader.val1, chunk_reader.rating, chunk_reader.count)
        write_u_chunk(u_chunk, u, output_dir)

    # MY_CUBOID  is the smallest sized cuboid, so it is used to compute M and Y cuboids.
    y_chunks = [{} for i in range(4)]
    for m in range(5):
        m_chunk = {}
        for y in [2006, 2007, 2008, 2009]:
            my_chunk_file = open(input_dir + f"/2D_CUBOIDS/MY_CUBOID/{my_to_chunk_id(m, y)}.txt")
            y_chunk = y_chunks[y-2006]
            for line in my_chunk_file:
                chunk_reader = ChunkLineReader(line)
                aggregate_into_chunk(y_chunk, chunk_reader.val2, chunk_reader.rating, chunk_reader.count)
                aggregate_into_chunk(m_chunk, chunk_reader.val1, chunk_reader.rating, chunk_reader.count)

            if m == 4:
                write_y_chunk(y_chunk, y, output_dir)
                y_chunks[y-2006] = None # free the memory
        write_m_chunk(m_chunk, m, output_dir)


def write_y_chunk(chunk, y, output_dir):
    y_chunk_file = open(f"{output_dir}/1D_CUBOIDS/Y_CUBOID/{y-2006 + 1}.txt", "w")
    y_chunk_file.write(chunk_dict_to_str(chunk))
    y_chunk_file.close()


def write_m_chunk(chunk, m, output_dir):
    m_chunk_file = open(f"{output_dir}/1D_CUBOIDS/M_CUBOID/{m}.txt", "w")
    m_chunk_file.write(chunk_dict_to_str(chunk))
    m_chunk_file.close()

def write_u_chunk(chunk, u, output_dir):
    u_chunk_file = open(f"{output_dir}/1D_CUBOIDS/U_CUBOID/{u}.txt", "w")
    u_chunk_file.write(chunk_dict_to_str(chunk))
    u_chunk_file.close()


def chunk_dict_to_str(chunk):
    return "\n".join(
        [f'{val1}\t{rating / agg_count}\t{count}' for val1, (rating, count, agg_count) in
         chunk.items()])


def aggregate_into_chunk(chunk, key, rating, count):
    if key not in chunk:
        chunk[key] = [rating, count, 1]
    else:
        chunk[key][0] += rating
        chunk[key][1] += count
        chunk[key][2] += 1

class ChunkLineReader:
    def __init__(self, line):
        line = line.replace("\n", "")
        vals = line.split("\t")

        self.val1 = vals[0]
        self.val2 = vals[1]
        self.rating = float(vals[2])
        self.count = int(vals[3])

def um_to_chunk_id(u, m) -> int:
    return u + m*5 + 1


def uy_to_chunk_id(u, y) -> int:
    return u + (y - 2006)*5 + 1


def my_to_chunk_id(m, y) -> int:
    return m + (y - 2006)*5 + 1

file_in = sys.argv[2]
file_out = sys.argv[4]
make_1d_cuboids(file_in, file_out)
