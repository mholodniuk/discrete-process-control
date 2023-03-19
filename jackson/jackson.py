from pathlib import Path
import numpy as np

from utils.models import Dataset, Task


def calculate_total_execution_time(task_dataset: Dataset) -> tuple[str, int]:
    sorted_tasks = sort_by_release_time(task_dataset.tasks)
    moments_of_task_termination = []
    for idx, task in enumerate(sorted_tasks):
        time = np.max((moments_of_task_termination[idx-1] if idx > 0 else 0, task.release_time)) + task.execution_time
        moments_of_task_termination.append(time)

    return (task_dataset.id, moments_of_task_termination[-1])

def sort_by_release_time(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda task: task.release_time)



def read_data_from_directory(path_str: str) -> list[Dataset]:
    files = [item.absolute() for item in Path(path_str).iterdir() if item.is_file()]
    data = []
    for file in files:
        with file.open() as f:
            current_file_data = []
            for line in f:
                if len(line.split()) != 2: continue
                nums = line.split()
                current_file_data.append((int(nums[0]), int(nums[1])))
        data.append(Dataset(file.name, create_tasks_from_tuple_list(current_file_data)))

    return data

def create_tasks_from_tuple_list(task_list: list[tuple[int, int]]) -> list[Task]:
    return [Task(raw_task_data[0], raw_task_data[1]) for raw_task_data in task_list]


for tasks in read_data_from_directory('./data'):
    print(calculate_total_execution_time(tasks))