# from pathlib import Path
# import json


# class ProcessTracker:

#     def __init__(self, tracker_file="processed_files.json"):

#         self.tracker_file = Path(tracker_file)

#         if not self.tracker_file.exists():

#             with open(self.tracker_file, "w") as f:

#                 json.dump([], f)

#         with open(self.tracker_file, "r") as f:

#             self.processed = set(json.load(f))

#     def is_processed(self, filename: str) -> bool:

#         return filename in self.processed

#     def mark_processed(self, filename: str):

#         self.processed.add(filename)

#         with open(self.tracker_file, "w") as f:

#             json.dump(
#                 sorted(list(self.processed)),
#                 f,
#                 indent=4,
#             )

from pathlib import Path
import json


class ProcessTracker:

    def __init__(
        self,
        tracker_file="processed_files.json",
    ):

        self.tracker_file = Path(tracker_file)

        self.processed = set()

        # ---------------------------------------
        # Create tracker if it doesn't exist
        # ---------------------------------------

        if not self.tracker_file.exists():

            with open(
                self.tracker_file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump([], f, indent=4)

        # ---------------------------------------
        # Load tracker safely
        # ---------------------------------------

        try:

            with open(
                self.tracker_file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                self.processed = set(data)

        except (json.JSONDecodeError, ValueError):

            print(
                "[WARNING] processed_files.json is empty or corrupted."
            )

            self.processed = set()

            with open(
                self.tracker_file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump([], f, indent=4)

    # ---------------------------------------

    def is_processed(
        self,
        filename: str,
    ) -> bool:

        return filename in self.processed

    # ---------------------------------------

    def mark_processed(
        self,
        filename: str,
    ):

        self.processed.add(filename)

        with open(
            self.tracker_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                sorted(self.processed),
                f,
                indent=4,
            )