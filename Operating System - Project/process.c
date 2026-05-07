// Modern processors use the POSIX.1-2008 (settimer(), sigaction(), waitpad(), kill())
#define _XOPEN_SOURCE 700

// Import necessary libraries
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

// Import custom made process library
#include "process.h"

// Simulated work function for child processes
void child_work(int id, int base_priority) {
    // Simulate different "weights" of work
    int work_factor = (6 - base_priority); // priority 1..5 -> factor 5..1

    // Announce start of child process
    printf("[Child %d | priority=%d | pid=%d] started.\n",
           id, base_priority, getpid());
    fflush(stdout);

    // Simulate work loop
    for (long iter = 0;; ++iter) {
        // Perform some CPU-intensive calculations
        double x = 0.0;
        for (int i = 0; i < work_factor * 10000; ++i) {
            x += sin(i) * cos(i);
        }

        // Periodically print status
        if (iter % 100 == 0) {
            printf("[Child %d | pid=%d] iter=%ld, x=%f\n",
                   id, getpid(), iter, x);
            fflush(stdout);
        }

        // Sleep briefly to simulate yielding CPU
        {
            struct timespec ts = {0, 2000L * 1000L};
            nanosleep(&ts, NULL);
        }
    }
}
