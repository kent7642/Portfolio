#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <sys/types.h>
#include <stdio.h>
#include <signal.h>   // for sig_atomic_t, signals
#include <sys/time.h> // for struct itimerval, ITIMER_REAL

#define MAX_PROCS 32

typedef enum {
    PROC_READY,
    PROC_RUNNING,
    PROC_FINISHED
} proc_state_t;

typedef struct {
    pid_t pid;
    int   priority;     // higher value = more likely to be scheduled
    proc_state_t state;
} proc_t;

// Global state (defined in scheduler.c)
extern proc_t processes[MAX_PROCS];
extern int num_procs;
extern int current_index;
extern FILE *log_file;

// Flags modified by signal handlers (defined in scheduler.c)
extern volatile sig_atomic_t need_resched;
extern volatile sig_atomic_t child_exited;
extern volatile sig_atomic_t shutdown_flag;

// Public API
void init_scheduler(int nprocs, int base_priority, const char *log_path);
void start_timer(long slice_ms);
void install_signal_handlers(void);
void scheduler_cleanup(void);

// Scheduler helper (main.c may call this)
int choose_next_index(void);

// Signal handler prototypes  <<< ADD THESE
void sigalrm_handler(int sig);
void sigchld_handler(int sig);
void sigint_handler(int sig);

#endif
