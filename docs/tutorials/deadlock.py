#!/usr/bin/env

import os
import threading
import time


def first_thread(lock1, lock2):
    print("Thread 1: Trying to acquire lock1")
    with lock1:
        print("Thread 1: lock1 acquired")

        time.sleep(1)

        print("Thread 1: Trying to acquire lock2")
        with lock2:
            print("Thread 1: lock2 acquired")
    print("Thread 1: Released both locks")


def second_thread(lock1, lock2):
    print("Thread 2: Trying to acquire lock2")
    with lock2:
        print("Thread 2: lock2 acquired")

        time.sleep(1)

        print("Thread 2: Trying to acquire lock1")
        with lock1:
            print("Thread 2: lock1 acquired")
    print("Thread 2: Released both locks")


if __name__ == "__main__":
    print(f"thread ID {os.getpid()}")
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    p1 = threading.Thread(target=first_thread, args=(lock1, lock2))
    p2 = threading.Thread(target=second_thread, args=(lock1, lock2))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Finished execution")
