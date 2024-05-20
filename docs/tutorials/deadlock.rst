Deadlock
========

Intro
-----

This lesson is meant to familiarize you with PyStack with a classical
problem of locks acquisition.


In this exercise, we will intentionally create a lock ordering issue,
which is a common way of causing a deadlock, where two or more threads
are waiting for each other to release resources, causing the program to
hang indefinitely.

Development Environment Setup
-----------------------------

Navigate to the `PyStack GitHub repo <https://github.com/bloomberg/pystack>`_ and get a copy of the
source code. You can either clone it, or just download the zip, whatever is your preference here.

You will also need a terminal with ``python3`` installed, preferably one of the latest versions.

Once you have the repo ready to navigate, ``cd`` into the docs/tutorials folder:

.. code:: shell

    cd docs/tutorials/

It is here where we will be running the tests and exercises for the remainder of the tutorial.
For reference here are the official `python3 venv docs <https://docs.python.org/3/library/venv.html>`_.
You can also just follow along with the commands below.

Let's go ahead and setup our virtual environment.

.. code:: shell

    python3 -m venv .venv

Once your virtual environment has been created, you can activate it like so:

.. code:: shell

    source .venv/bin/activate

You can confirm activation was successful if your terminal prompt is prefixed with ``(.venv)``.
With our virtual environment ready, we can go ahead and install all the dependencies required
for the tutorial.

.. code:: shell

    python3 -m pip install -r requirements-tutorial.txt

Keep your virtual environment activated for the rest of the tutorial, and you should be able to run
any of the commands in the exercises.

PyStack remote use
------------------

PyStack remote has the ability to analyze the status of a running (remote) process.

Executing the deadlock
^^^^^^^^^^^^^^^^^^^^^^

In the ``tutorials`` directory, there will be a script called ``deadlock.py``:

.. include:: deadlock.py
   :literal:

Assuming that we are in the ``tutorials`` directory, we can run the deadlock script with:

.. code:: shell

    python3 deadlock.py

This script will intentionally perform a deadlock and the first message will contain the process ID.
Another option is to find it with:

.. code:: shell

    ps aux | grep deadlock.py

After the deadlock occurs we can use the PyStack command to analyze the
process (replace <PID> with the process ID from the previous step):

.. code:: shell

    pystack remote <PID>


Potentially it will appear an ``Operation not permitted`` error. If it is your case use this command instead:

.. code:: shell

    sudo -E pystack remote <PID>

The output should be this:

.. code:: shell

    Thread 1: Trying to acquire lock1
    Thread 1: lock1 acquired
    Thread 2: Trying to acquire lock2
    Thread 2: lock2 acquired
    Thread 1: Trying to acquire lock2
    Thread 2: Trying to acquire lock1


Understanding the results
^^^^^^^^^^^^^^^^^^^^^^^^^

The excepted result is the following code:

.. code:: shell

    Traceback for thread 518222 (python3) [] (most recent call last):
        (Python) File "/<pyhon_env_path>/threading.py", line 966, in _bootstrap
            self._bootstrap_inner()
        (Python) File "/<pyhon_env_path>/threading.py", line 1009, in _bootstrap_inner
            self.run()
        (Python) File "/<pyhon_env_path>/threading.py", line 946, in run
            self._target(*self._args, **self._kwargs)
        (Python) File "/<path_to_tutorials>/deadlock.py", line 30, in process2
            lock1.acquire()

    Traceback for thread 518221 (python3) [] (most recent call last):
        (Python) File "/<pyhon_env_path>/threading.py", line 966, in _bootstrap
            self._bootstrap_inner()
        (Python) File "/<pyhon_env_path>/threading.py", line 1009, in _bootstrap_inner
            self.run()
        (Python) File "/<pyhon_env_path>/threading.py", line 946, in run
            self._target(*self._args, **self._kwargs)
        (Python) File "/<path_to_tutorials>/deadlock.py", line 16, in process1
            lock2.acquire()

    Traceback for thread 518220 (python3) [] (most recent call last):
        (Python) File "/<path_to_tutorials>/deadlock.py", line 46, in <module>
            p1.join()
        (Python) File "/<pyhon_env_path>/threading.py", line 1089, in join
            self._wait_for_tstate_lock()
        (Python) File "/<pyhon_env_path>/threading.py", line 1109, in _wait_for_tstate_lock
            if lock.acquire(block, timeout):

Notice that each section is displaying a running thread.
Each thread has a flow of actions that can be audited to find the potential problem:
 - The thread 518222 is trying to acquire lock1 but is blocked because lock1 is already held by the other thread.
 - The thread 518221 is trying to acquire lock2 but is blocked because lock2 is already held by the other thread.
 - The main thread 518220 is calling join() on p1, waiting for it to finish.  However, p1 cannot finish because it is stuck waiting to acquire a lock, leading to a deadlock.

This way we can successful diagnose that there are a improper ordering of lock acquisition.
