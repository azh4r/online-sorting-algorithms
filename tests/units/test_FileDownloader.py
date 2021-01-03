import unittest
import FileDownloader

class TestFileDownloader:
    # Test that process_chunks returns the lines and the leftover chunk
    def test_FileDownloader_process_chunk(self):
        chunk = b'sfks 40\naslkfdd 30\nsdfs'
        leftover = b'akj'
        is_last = False

        # text_lines, new_leftover = FileDownloader.process_chunk(chunk, is_last, leftover)
        expected_text_lines = ['akjsfks 40','aslkfdd 30']
        expected_leftover = b'sdfs'
        assert FileDownloader.process_chunk(chunk, is_last, leftover) == (expected_text_lines, expected_leftover)


    def test_FileDownloader_process_last_chunk(self):
        chunk = b'sfks 40\naslkfdd 30\nsdfs'
        leftover = b'akj'
        is_last = True

        result_text_lines, result_leftover = FileDownloader.process_chunk(chunk, is_last, leftover)
        expected_text_lines = ['akjsfks 40','aslkfdd 30', 'sdfs']
        expected_leftover = b'akj'
        assert result_text_lines == expected_text_lines
        assert result_leftover == expected_leftover


if __name__ == '__main__':
    unittest.main
