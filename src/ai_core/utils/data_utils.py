import json
import os

class DataUtils:
    @staticmethod
    def load_json(file_path):
        # Load data from a JSON file.
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            print(f"File not found: {file_path}")
            return None

    @staticmethod
    def save_json(data, file_path):
        # Save data to a JSON file.
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_path}")

    @staticmethod
    def merge_datasets(dataset1, dataset2):
        # Merge two datasets (lists of dictionaries).
        return dataset1 + dataset2

    @staticmethod
    def filter_data(data, filter_function):
        # Filter data based on a custom filter function.
        return list(filter(filter_function, data))

if __name__ == "__main__":
    # Example usage
    data1 = DataUtils.load_json('data/part1.json')
    data2 = DataUtils.load_json('data/part2.json')

    if data1 and data2:
        merged_data = DataUtils.merge_datasets(data1, data2)
        DataUtils.save_json(merged_data, 'data/merged_data.json')

    # Example filter function
    def example_filter(entry):
        return 'important' in entry['text']

    filtered_data = DataUtils.filter_data(merged_data, example_filter)
    DataUtils.save_json(filtered_data, 'data/filtered_data.json')
