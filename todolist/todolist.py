from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
 
Base = declarative_base()
 
 
class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
def get_menu_choice():
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")
    choice = int(input())
    return choice
 
def print_all_tasks(task_rows, with_date=False):
    if len(task_rows) == 0:
        print("Nothing to do!")
    elif not with_date:
        for index, task_row in enumerate(task_rows):
            print(f"{index + 1}. {task_row.task}")
    elif with_date:
        for index, task_row in enumerate(task_rows):
            print(f"{index + 1}. {task_row.task}. {task_row.deadline.day} {task_row.deadline.strftime('%b')}")
 
while True:
    choice = get_menu_choice()
    if choice == 1:  # print today's tasks
        date = datetime.today().date()
        task_rows = session.query(TaskTable).filter(TaskTable.deadline == date).all()
        print("Today {date.day} {date.strftime('%b')}:")
        print_all_tasks(task_rows)
        print()
 
    elif choice == 2:  # print this week's tasks
        today = datetime.today().date()
        for dif in range(7):
            date = datetime.today().date() + timedelta(days=dif)
            print(f"{date.strftime('%A')} {date.day} {date.strftime('%b')}:")
            task_rows = session.query(TaskTable).filter(TaskTable.deadline == date).all()
            print_all_tasks(task_rows)
            print()
 
    elif choice == 3:  # print all tasks
        task_rows = session.query(TaskTable).order_by(TaskTable.deadline).all()
        print_all_tasks(task_rows, True)
        print()
 
    elif choice == 4:  # print missed tasks
        today = datetime.today().date()
        task_rows = session.query(TaskTable).filter(TaskTable.deadline < today).all()
        print("Missed tasks:")
        print_all_tasks(task_rows, True)
        print()
 
    elif choice == 5:  # add task to database
        task_string = input("Enter task")
        task_date = input("Enter deadline")
        task_date = datetime.strptime(task_date, '%Y-%m-%d')
        new_task_row = TaskTable(task=task_string, deadline=task_date)
        session.add(new_task_row)
        session.commit()
        print("The task has been added!")
        print()
 
    elif choice == 6:  # delete task
        print("Choose the number of the task you want to delete:")
        task_rows = session.query(TaskTable).all()
        print_all_tasks(task_rows)
        delete_index = int(input()) - 1
        session.delete(task_rows[delete_index])
        session.commit()
        print("The task has been deleted!")
        print()
 
    elif choice == 0:  # exit
        break
