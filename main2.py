import json
import datetime
from functools import reduce


with open('todos.json', "r") as f:
  data = json.load(f)


def group_tasks_by_user(user_tasks):

    grouped_users_tasks = {}
    for task in user_tasks:
        if "userId" in task:
            user_id = task['userId']
            tasks = grouped_users_tasks[user_id] if user_id  in grouped_users_tasks else []
            tasks.append(task)
            grouped_users_tasks[task['userId']] = tasks
    return grouped_users_tasks


def group_task_by_completed():

    completed_task = {}
    uncompleted_task = {}
    for user_id in group_tasks_by_user(data):
        tasks = group_tasks_by_user(data)[user_id]
        completed_task[user_id] = reduce((lambda x, y: str(x) + "\n" + str(y)),
                        map((lambda t: t["title"] if len(t["title"]) < 50 else t["title"][0:50] + "..."), filter((lambda t: t['completed']), tasks)))
        uncompleted_task[user_id] = reduce((lambda x, y: str(x) + "\n" + str(y)),
                        map((lambda t: t["title"] if len(t["title"]) < 50 else t["title"][0:50] + "..."), filter((lambda t: t['completed'] == False), tasks)))
    return completed_task, uncompleted_task



def write_in_file(completed_task, uncompleted_task):
    for user_id in group_tasks_by_user(data):
        today_data = datetime.datetime.today()
        with open(str(user_id) + str(today_data.strftime('_%Y-%m-%dT%H-%M')) + ".txt", 'w', encoding='utf-8') as f:
            f.write("#Сотрудник №" + str(user_id) + "\n")
            f.write(str(today_data.strftime('%d.%m.%Y %H:%M')) + "\n")
            f.write("\n")
            f.write("## Завершённые задачи:\n")
            f.write(completed_task[user_id] + "\n")
            f.write("\n")
            f.write("## Оставшиеся задачи:\n")
            f.write(uncompleted_task[user_id])


def main():
    completed_task, uncompleted_task = group_task_by_completed()
    write_in_file(completed_task, uncompleted_task)


if __name__ == '__main__':
  main()