#ifndef SCHEDULER_UTILS_H
#define SCHEDULER_UTILS_H

#include <sys/types.h>
#include <stdio.h>

// Set the FILE* used for logging. Call this once after opening the log file.
void set_log_file(FILE *f);

// Log a textual event (written to the log file if set).
void log_event(const char *msg);

// Send a signal to a pid and log success/failure.
void safe_kill(pid_t pid, int sig, const char *desc);

#endif
