from typing import List

import aiofiles
import csv
import io


class CsvClient:
    def __init__(self, file_path: str, headers: List[str], delimiter=",", chunk_size=1000):
        self.file_path = file_path
        self.headers = headers
        self.delimiter = delimiter
        self.chunk_size = chunk_size

    async def read_large_csv(self):
        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
            is_first_chunk = True
            current_chunk = []
            async for line in file:
                if is_first_chunk:
                    is_first_chunk = False  # After the first line is read, set to False
                    continue  # Skip the first line
                current_chunk.append(line)
                if len(current_chunk) >= self.chunk_size:
                    for processed_row in self.process_chunk(current_chunk):
                        yield processed_row
                    current_chunk = []  # Reset chunk after processing
            # Process any remaining lines in the last chunk
            if current_chunk:
                for processed_row in self.process_chunk(current_chunk):
                    yield processed_row

    def process_chunk(self, chunk):
        chunk_str = '\n'.join(chunk)
        file_like_object = io.StringIO(chunk_str)
        reader = csv.DictReader(file_like_object, delimiter=self.delimiter, fieldnames=self.headers)
        for row in reader:
            processed_row = self.process_row(row)
            yield processed_row

    def process_row(self, row):
        # Add specific row processing here if needed

        processed_row = {key: value.strip() for key, value in row.items()}  # Example processing
        return processed_row
