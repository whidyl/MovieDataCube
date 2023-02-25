from main import *
from compute2DCuboid import make_2d_cuboids
from compute1DCuboid import make_1d_cuboids

def test__get_all_user_ids__has_expected_size():
    size = len(get_all_user_ids())

    assert size == 13676


def test__get_user_partitions__is_sorted_and_ps_have_expected_sizes():
    partitions = get_user_partitions()

    assert len(partitions) == 5
    assert (all(is_id_list_sorted(partition) for partition in partitions))
    assert (len(partitions[0]) == 3000)
    assert (all(len(partition) <= 3000 for partition in partitions))


def test__get_movie_partitions__is_sorted_and_ps_have_expected_sizes():
    partitions = get_movie_partitions()

    assert len(partitions) == 5
    assert (all(is_id_list_sorted(partition) for partition in partitions))
    assert (len(partitions[0]) == 2500)
    assert (all(len(partition) <= 2500 for partition in partitions))


def is_id_list_sorted(l):
    return all(l[i] <= l[i + 1] for i in range(len(l) - 1))


def test_get_partition_of_user_id__returns_expected_for_each_group():
    partitions = get_user_partitions()

    for p in range(4):
        for user_id in partitions[p]:
            assert get_partition_of_user_id(user_id) == p


def test_get_partition_of_movie_id__returns_expected_for_each_group():
    partitions = get_movie_partitions()

    for p in range(4):
        for movie_id in partitions[p]:
            assert get_partition_of_movie_id(movie_id) == p


def test_make_base_cuboid__chunks_are_unique_and_correct_count():
    chunks = make_base_cuboid().keys()

    assert len(chunks) == len(set(chunks))
    assert len(chunks) == 5 * 5 * 4


def test__make_base_cuboid__has_expected_keys_and_lengths():
    cuboid = make_base_cuboid()

    c1 = cuboid[(0, 0, 2006)]
    c2 = cuboid[(4, 4, 2007)]
    c3 = cuboid[(3, 2, 2008)]

    assert all([get_partition_of_user_id(u_id) == 0 for u_id, m_id, year, rating in c1])
    assert all([year == 2006 for u_id, m_id, year, rating in c1])
    assert all([get_partition_of_movie_id(m_id) == 4 for u_id, m_id, year, rating in c2])
    assert all([get_partition_of_user_id(u_id) == 3 for u_id, m_id, year, rating in c3])


def test__make_2d_cuboids__has_expected_sizes():
    cuboids = make_2d_cuboids()

    assert len(cuboids) == 3
    assert len(cuboids[0].keys()) == 5*5


def test__make_2d_cuboids__cuboids_has_expected_data():
    cuboids_2d = make_2d_cuboids()
    mu_cuboid = cuboids_2d[0]
    my_cuboid = cuboids_2d[1]
    uy_cuboid = cuboids_2d[2]

    assert all([get_partition_of_user_id(u_id) == 0 for m_id, u_id in mu_cuboid[(0, 0)].keys()])
    assert all([get_partition_of_user_id(u_id) == 1 for u_id, year in uy_cuboid[(1, 2006)].keys()])
    assert True


def test__make_1d_cuboids__cuboids_has_expected_data_size():
    cuboids_1d = make_1d_cuboids()
    u_cuboid = cuboids_1d[0]
    m_cuboid = cuboids_1d[1]
    y_cuboid = cuboids_1d[2]

    assert len(u_cuboid[0]) == 3000
    #assert len(m_cuboid[0]) == 2500
    #assert len(y_cuboid[2006]) == 4
    assert True


def test__chunk_line_to_rating__typical_chunk_line__has_expected_data():
    chunk_line = '9\t50\t2006\t5.0'

    rating = chunk_line_to_rating(chunk_line)

    assert rating == 5.0


def umy_to_chunk_id(u, m, y):
    return u + m*5 + (y-2006)*5*5 + 1


def test_umy_to_chunk_id():
    assert umy_to_chunk_id(0, 0, 2006) == 1
    assert umy_to_chunk_id(4, 0, 2006) == 5
    assert umy_to_chunk_id(0, 1, 2006) == 6
    assert umy_to_chunk_id(3, 1, 2006) == 9
    assert umy_to_chunk_id(0, 3, 2006) == 16
    assert umy_to_chunk_id(4, 4, 2006) == 25
    assert umy_to_chunk_id(4, 4, 2009) == 64

def uy_to_chunk_id(u, y) -> int:
    """converts into a chunk_id for 0 to 100 counting up by user first, then movie, then year."""
    return u + (y - 2006)*5 + 1


def test_uy_to_chunk_id():
    assert uy_to_chunk_id(0, 2006) == 1
    assert uy_to_chunk_id(4, 2006) == 5
    assert uy_to_chunk_id(0, 2007) == 6
    assert uy_to_chunk_id(4, 2009) == 20


def test_compute_2D_cuboid():
    make_2d_cuboids("./Output",  "./Output")

def test_compute_1D_cuboid():
    make_1d_cuboids("./Output",  "./Output")
