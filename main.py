from collections.abc import Set
import datetime
from enum import Enum


def make_base_cuboid():
    base_cube = {}

    for u in range(5):
        for m in range(5):
            for y in [2006, 2007, 2008, 2009]:
                base_cube[(u, m, y)] = []

    ratings_file = open("./MovieRatingsData/ratings.txt", "r")
    for line in ratings_file:
        line_data = get_data_from_rating_line(line)
        u_m_y_key = (line_data["user_partition"], line_data["movie_partition"], line_data["year"])
        if line_data["year"] == 2005:
            continue
        base_cube[u_m_y_key].append(make_1d_chunk_cell(line_data))
    ratings_file.close()

    return base_cube


def get_data_from_rating_line(line):
    vals = line.split("::")
    user_id, movie_id = int(vals[0]), int(vals[1])
    return {
        "user_id": user_id,
        "movie_id": movie_id,
        "user_partition": get_partition_of_user_id(user_id),
        "movie_partition": get_partition_of_movie_id(movie_id),
        "year": datetime.datetime.fromtimestamp(int(vals[3])).year,
        "rating": float(vals[2])
    }


def make_chunk_line(line_data):
    return str(line_data["user_id"]) + "\t" + str(line_data["movie_id"]) + "\t" + str(line_data["year"]) + "\t" + str(
        line_data["rating"]) + "\t"


def make_1d_chunk_cell(line_data):
    return line_data["user_id"], line_data["movie_id"], line_data["year"], line_data["rating"]


def make_2d_cuboids():
    base_cube = make_base_cuboid()
    um_cuboid, my_cuboid, uy_cuboid = init_2d_cubes()

    for u in range(5):
        for m in range(5):
            for y in [2006, 2007, 2008, 2009]:
                base_chunk = base_cube[(u, m, y)]
                um_chunk, my_chunk, uy_chunk = um_cuboid[(u, m)], my_cuboid[(m, y)], uy_cuboid[(u, y)]

                for user_id, movie_id, year, rating in base_chunk:
                    aggregate_into_chunk(um_chunk, (user_id, movie_id), rating)
                    aggregate_into_chunk(my_chunk, (movie_id, year), rating)
                    aggregate_into_chunk(uy_chunk, (user_id, year), rating)

    return um_cuboid, my_cuboid, uy_cuboid


def make_1d_cuboids():
    um_cuboid, my_cuboid, uy_cuboid = make_2d_cuboids()

    u_cuboid = {u: {} for u in range(5)}
    m_cuboid = {m: {} for m in range(5)}
    y_cuboid = {y: {} for y in [2006, 2007, 2008, 2009]}

    for u in range(5):
        u_chunk = u_cuboid[u]
        for y in [2006, 2007, 2008, 2009]:
            for (user_id, year), (rating, count) in uy_cuboid[(u, y)].items():
                aggregate_into_chunk(u_chunk, user_id, rating, count)

    for m in range(5):
        m_chunk = m_cuboid[m]
        for y in [2006, 2007, 2008, 2009]:
            y_chunk = y_cuboid[y]
            for (movie_id, year), (rating, count) in my_cuboid[(m, y)].items():
                aggregate_into_chunk(m_chunk, movie_id, rating, count)
                aggregate_into_chunk(y_chunk, year, rating, count)

    return u_cuboid, m_cuboid, y_cuboid


def init_2d_cubes():
    um_cuboid = {}
    for u in range(5):
        for m in range(5):
            um_cuboid[(u, m)] = {}

    my_cuboid = {}
    for m in range(5):
        for y in [2006, 2007, 2008, 2009]:
            my_cuboid[(m, y)] = {}

    uy_cuboid = {}
    for u in range(5):
        for y in [2006, 2007, 2008, 2009]:
            uy_cuboid[(u, y)] = {}

    return um_cuboid, my_cuboid, uy_cuboid


def aggregate_into_chunk(chunk, key, rating, count=1):
    if key not in chunk:
        chunk[key] = [rating, count]
    else:
        chunk[key][0] += rating
        chunk[key][1] += count


def chunk_line_to_rating(chunk_line):
    line_stripped = chunk_line.split("\t")
    rating = float(line_stripped[3])
    return rating


def get_all_user_ids() -> set:
    return get_all_ids("./MovieRatingsData/ratings.txt")


def get_all_movie_ids() -> set:
    return get_all_ids("./MovieRatingsData/movies.txt")


def get_all_ids(file_name):
    ids = set()

    ratings_file = open(file_name, "r", encoding="utf8")
    for line in ratings_file:
        id_str = line.split("::")[0]
        ids.add(int(id_str))
    ratings_file.close()
    return ids


def get_user_partitions():
    return split_into_five_partitions(get_all_user_ids(), 3000)


def get_movie_partitions():
    return split_into_five_partitions(get_all_movie_ids(), 2500)


def split_into_five_partitions(ids_set, p_size):
    ids = list(ids_set)
    ids.sort()
    return [ids[:p_size], ids[p_size:p_size * 2], ids[p_size * 2:p_size * 3], ids[p_size * 3:p_size * 4],
            ids[p_size * 4:]]


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
