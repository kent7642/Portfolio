os-scheduler
===========

Small educational preemptive scheduler using fork, signals and setitimer.

Build
-----

Run from project root:

```bash
make
```

This compiles `main.c`, `scheduler.c` and `process.c` and produces the `scheduler` binary.

Run
---

Usage:

```bash
./scheduler <num_processes> <timeslice_ms> <logfile>
```

Example:

```bash
./scheduler 4 100 scheduler.log
```

This starts 4 child processes with a 100ms timeslice and logs scheduler events to `scheduler.log`.

Convenience targets
-------------------
- `make run` — build and run with an example argument set (`4 100 scheduler.log`).
- `make test` — build and run a 5-second smoke test (requires `timeout`).
- `make clean` — remove the binary and log.

Notes
---------------------
- Child processes in `process.c` currently run an infinite loop — use `timeout` to limit runtime in tests.
- To stop the scheduler interactively, press Ctrl-C (SIGINT). The program will attempt a graceful shutdown.
