// Enable GNU extensions for modern POSIX features
#define _GNU_SOURCE

// Import custom made scheduler and process libraries
#include "scheduler.h"
#include "process.h"
#include "scheduler_utils.h"

// Import necessary libraries
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <errno.h>

// Array that holds scheduler's process control blocks
proc_t processes[MAX_PROCS];

// Number of processes managed by the scheduler
int num_procs = 0;

// Index of the currently running process
int current_index = -1;

// File pointer for the log file (kept for direct checks by this module)
FILE *log_file = NULL;

// Flags defined here, declared extern in scheduler.h
volatile sig_atomic_t need_resched   = 0;
volatile sig_atomic_t child_exited   = 0;
volatile sig_atomic_t shutdown_flag  = 0;

// Note: logging and safe_kill are provided by scheduler_utils.c

// Scheduler's process selection algorithm (priority-based round-robin)
int choose_next_index(void) {
    // Start searching from the next process after the current one
    int start = current_index;

    // Track the best candidate index and its priority
    int best_idx = -1;
    int best_prio = -1;

    // Loop through all processes once
    for (int i = 0; i < num_procs; ++i) {
        // Calculate the index in a circular manner
        int idx = (start + 1 + i) % num_procs;

        // Check if the process is ready to run
        if (processes[idx].state == PROC_READY) {
            // If this process has a higher priority, select it
            if (processes[idx].priority > best_prio) {
                // Update the best candidate
                best_prio = processes[idx].priority;
                best_idx = idx;
            }
        }
    }

    // Return the index of the selected process based on the algorithm
    return best_idx;
}

// Initialize the scheduler and fork child processes
void init_scheduler(int nprocs, int base_priority, const char *log_path) {
    // Check for maximum process limit
    if (nprocs > MAX_PROCS) {
        fprintf(stderr, "Max %d processes supported\n", MAX_PROCS);
        exit(EXIT_FAILURE);
    }

    // Open the log file for writing
    log_file = fopen(log_path, "w");
    if (!log_file) {
        perror("fopen log file");
        exit(EXIT_FAILURE);
    }

    // Inform the shared logging utility about the opened file so it can
    // write events. We keep `log_file` here for checks in this module but
    // forward it to the utils module.
    set_log_file(log_file);

    // Set the number of processes
    num_procs = nprocs;

    // Fork child processes with assigned priorities
    for (int i = 0; i < num_procs; ++i) {
        // Assign priority and initial state
        processes[i].priority = base_priority + (i % 3);
        processes[i].state = PROC_READY;

        // Fork the child process
        pid_t pid = fork();
        
        if (pid < 0) { // Fork error
            perror("fork");
            exit(EXIT_FAILURE);
        } else if (pid == 0) { // Child process
            child_work(i, processes[i].priority);
            _exit(0);
        } else { // Parent process
            processes[i].pid = pid;
            char buf[128];
            snprintf(buf, sizeof(buf),
                     "[Parent] Forked child index=%d pid=%d prio=%d",
                     i, pid, processes[i].priority);
            log_event(buf);
        }
    }

    // stop all children initially (log success/failure)
    for (int i = 0; i < num_procs; ++i) {
        safe_kill(processes[i].pid, SIGSTOP, "initial SIGSTOP");
    }
}

// Start the timer for scheduling time slices
void start_timer(long slice_ms) {
    // Convert milliseconds to seconds and microseconds
    struct itimerval it;
    long sec = slice_ms / 1000;
    long usec = (slice_ms % 1000) * 1000;

    // Set the timer interval and initial expiration
    it.it_interval.tv_sec  = sec;
    it.it_interval.tv_usec = usec;
    it.it_value            = it.it_interval;

    // Check for errors in setting the timer
    if (setitimer(ITIMER_REAL, &it, NULL) < 0) {
        perror("setitimer");
        exit(EXIT_FAILURE);
    }
}

// Install signal handlers for SIGALRM, SIGCHLD, and SIGINT
void install_signal_handlers(void) {
    struct sigaction sa;

    // Setup SIGALRM handler
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = sigalrm_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    if (sigaction(SIGALRM, &sa, NULL) < 0) {
        perror("sigaction SIGALRM");
        exit(EXIT_FAILURE);
    }

    // Setup SIGCHLD handler
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    if (sigaction(SIGCHLD, &sa, NULL) < 0) {
        perror("sigaction SIGCHLD");
        exit(EXIT_FAILURE);
    }

    // Setup SIGINT handler
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    if (sigaction(SIGINT, &sa, NULL) < 0) {
        perror("sigaction SIGINT");
        exit(EXIT_FAILURE);
    }
}

// Cleanup function to stop timer and terminate child processes
void scheduler_cleanup(void) {
    // Stop the timer
    struct itimerval it = {0};
    setitimer(ITIMER_REAL, &it, NULL);

    // Terminate all child processes
    for (int i = 0; i < num_procs; ++i) {
        if (processes[i].state != PROC_FINISHED) {
            safe_kill(processes[i].pid, SIGKILL, "cleanup SIGKILL");
        }
    }

    // Close the log file if opened
    if (log_file) {
        log_event("[Parent] Scheduler cleanup complete.");
        fclose(log_file);
        log_file = NULL;
        /* Clear the utils' copy of the log pointer as well. */
        set_log_file(NULL);
    }
}

// Signal handler for SIGALRM (timer expiration)
void sigalrm_handler(int sig) {
    (void)sig;
    need_resched = 1;
}

// Signal handler for SIGCHLD (child process state change)
void sigchld_handler(int sig) {
    (void)sig;
    child_exited = 1;
}

// Signal handler for SIGINT (interrupt signal)
void sigint_handler(int sig) {
    (void)sig;
    shutdown_flag = 1;
}
