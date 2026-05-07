// Modern processors use the POSIX.1-2008 (settimer(), sigaction(), waitpad(), kill())
#define _XOPEN_SOURCE 700

// Import necessary libraries
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

// Import custom made scheduler library
#include "scheduler.h"
// Import shared scheduler utilities (logging + safe_kill)
#include "scheduler_utils.h"

// Checks that all processes should be finished
static int all_finished(void) {
    for (int i = 0; i < num_procs; ++i) {
        if (processes[i].state != PROC_FINISHED) {
            return 0;
        }
    }
    return 1;
}

// Main program code
int main(int argc, char *argv[]) {
    // Get arguments when pogram is trying to be compiled (The number of process, timeslice for the scheduler, logfile name)
    if (argc < 4) {
        fprintf(stderr,
                "Usage: %s <num_processes> <timeslice_ms> <logfile>\n",
                argv[0]);
        return EXIT_FAILURE;
    }

    // Convert string to integer for number of processes and store it
    int  nprocs    = atoi(argv[1]);

    // Convert string to long for time slice and store it
    long slice_ms  = atol(argv[2]);

    // Store log filename
    const char *log_path = argv[3];

    // Check if the number of process is between 1 and 32
    if (nprocs <= 0 || nprocs > MAX_PROCS) {
        fprintf(stderr, "num_processes must be 1..%d\n", MAX_PROCS);
        return EXIT_FAILURE;
    }

    // Check if the time slice is at least 1ms so the scheduler could work
    if (slice_ms <= 0) {
        fprintf(stderr, "timeslice_ms must be > 0\n");
        return EXIT_FAILURE;
    }

    // Show that the scheduler is starting
    printf("Starting scheduler: nprocs=%d, slice=%ldms, logfile=%s\n",
           nprocs, slice_ms, log_path);

    // Installs the signal_handlers and initialize schedulers (function is called from scheduler.h and is defined in scheduler.c)
    install_signal_handlers();
    init_scheduler(nprocs, 3, log_path);
    
    // Number of process that is already run
    current_index = 0;

    // The state of the process that is being run
    processes[current_index].state = PROC_RUNNING;

    // Resumes the child process that is about to be run
    safe_kill(processes[current_index].pid, SIGCONT, "initial resume");

    // Timer starts for child process current_index
    start_timer(slice_ms);
    
    // Loop the processes while CTRL + C (shutdown_flag) is not pressed or process is not finished
    while (!shutdown_flag && !all_finished()) {

        // Checks if sigchId_handler receives the signal (when it receives the signal it means child process has exited) 
        if (child_exited) {

            // Reset the flag
            child_exited = 0;

            // Initialization of variable for status and process id
            int status;
            pid_t pid;

            // Loops all finished or exited child process and flags it setting it to finished 
            // pid > 0 means exited successfully
            // pid == 0 means no child exited
            // pid < 0 or pid == -1 means error
            while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {

                // Matches the process id exited with our process array and sets it to finished
                for (int i = 0; i < num_procs; ++i) {

                    // Process id finished found in our process array
                    if (processes[i].pid == pid) {

                        // Set it the state to finished
                        processes[i].state = PROC_FINISHED;
                        break;
                    }
                }
            }
        }

        // Checks if sigalrm_handler receives the signal (when it receives the signal it means time to pick a new process)
        if (need_resched) {

                // Reset the flag
                need_resched = 0;

                // Pick the next candidate first so we don't stop the current
                // process and then find there's nobody ready to run.
                int next = choose_next_index();

                // If a next process is found and it's different from the current,
                // preempt the current and resume the next.
                if (next >= 0 && next != current_index) {
                    if (current_index >= 0 &&
                        processes[current_index].state == PROC_RUNNING) {
                        safe_kill(processes[current_index].pid, SIGSTOP, "preempt SIGSTOP");
                        processes[current_index].state = PROC_READY;
                    }

                    current_index = next;
                    processes[current_index].state = PROC_RUNNING;
                    safe_kill(processes[current_index].pid, SIGCONT, "resume SIGCONT");
                }

                // If next == -1 (no ready process), leave the current process
                // running (do nothing). This prevents leaving all children
                // stopped when there is nobody ready to schedule.
        }

        // Pause the scheduler until a signal is received
        pause();
    }

    // Show that the scheduler is shutting down
    printf("Shutting down scheduler...\n");

    // Clean up resources used by the scheduler
    scheduler_cleanup();

    // Exit successfully
    return EXIT_SUCCESS;
}
