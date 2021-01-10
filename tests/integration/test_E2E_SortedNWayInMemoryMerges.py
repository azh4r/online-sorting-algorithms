import pytest
from ProcessSortedNWayInMemoryMerge import SortedNWayMemoryMerge


@pytest.mark.integration_test
def test_with_50_records_SinglePriorityQueue(capsys):
    sorted_nway_memory_merge = SortedNWayMemoryMerge()
    sorted_nway_memory_merge.process("http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_50.txt", 8, 500, 5)
    captured = capsys.readouterr()
    assert captured.out == '235a4ac593befd55cdf\n78eab4ccbdd98fa911e\ndf7b4609da6e60b91c3\n0a3952404ca98f1e64f\n70da387aeab65eb5f4f\n'

@pytest.mark.integration_test
def test_with_100_records_SinglePriorityQueue(capsys):
    sorted_nway_memory_merge = SortedNWayMemoryMerge()
    sorted_nway_memory_merge.process("http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_100.txt", 8, 500, 5)
    captured = capsys.readouterr()
    # print(captured.out)
    assert captured.out == 'f5e91e10eaa840419d8\na03beec7f862a4486df\n235a4ac593befd55cdf\n78eab4ccbdd98fa911e\n'


@pytest.mark.integration_test
def test_with_500_records_SinglePriorityQueue(capsys):
    sorted_nway_memory_merge = SortedNWayMemoryMerge()
    sorted_nway_memory_merge.process("http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_500.txt", 8, 500, 5)
    captured = capsys.readouterr()
    assert captured.out == '21d8d9157863db8d566\n60d84237d76fc2a434f\n96e966f05ff7b1a7811\n9caa765cfdfee3c4227\n87787a9e0a5f0fcf3c1\n'
    
@pytest.mark.integration_test
def test_with_1000_records_SinglePriorityQueue(capsys):
    sorted_nway_memory_merge = SortedNWayMemoryMerge()
    sorted_nway_memory_merge.process("http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_1000.txt", 8, 500, 5)
    captured = capsys.readouterr()
    assert captured.out == '21d8d9157863db8d566\n60d84237d76fc2a434f\n100ae6cdd3eb8f64e55\n'

@pytest.mark.integration_test
def test_with_1500_records_SinglePriorityQueue(capsys):
    sorted_nway_memory_merge = SortedNWayMemoryMerge()
    sorted_nway_memory_merge.process("http://127.0.0.1:5500/test_data/spacemaps_technical_challenge_1500.txt", 8, 500, 5)
    captured = capsys.readouterr()
    assert captured.out == '21d8d9157863db8d566\nd418cc1a140a1e27672\n95b970f2883b8e0110d\n'


