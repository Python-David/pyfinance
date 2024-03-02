import csv
import io
from typing import List, Tuple

import aiofiles


class CsvClient:
    def __init__(
        self, file_path: str, headers: List[str], delimiter=",", chunk_size=1000
    ):
        self.file_path = file_path
        self.headers = headers
        self.delimiter = delimiter
        self.chunk_size = chunk_size

    async def read_large_csv(self):
        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
            is_first_chunk: bool = True
            current_chunk: List = []
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
        chunk_str = "\n".join(chunk)
        file_like_object = io.StringIO(chunk_str)
        reader = csv.DictReader(
            file_like_object, delimiter=self.delimiter, fieldnames=self.headers
        )
        for row in reader:
            processed_row = self.process_row(row)
            yield processed_row

    def process_row(self, row):
        processed_row = {
            key: value.strip() for key, value in row.items()
        }  # Example processing
        return processed_row

    async def write_to_csv(self, data) -> Tuple[bool, str]:
        """Write data to a CSV file."""
        try:
            async with aiofiles.open(
                self.file_path, mode="w", encoding="utf-8"
            ) as file:
                # Use an in-memory StringIO to leverage csv.DictWriter
                output = io.StringIO()
                writer = csv.DictWriter(
                    output, fieldnames=self.headers, delimiter=self.delimiter
                )

                writer.writeheader()  # Write the headers
                for row in data:
                    writer.writerow(row)  # Write each row

                # Go to the beginning of the StringIO buffer
                output.seek(0)
                # Write the contents of the StringIO buffer to the file
                await file.write(output.read())
            return True, "File written successfully."
        except Exception as e:
            return False, f"Failed to write to CSV: {e}"
