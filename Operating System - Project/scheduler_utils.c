#include "scheduler_utils.h"
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <signal.h>
#include <unistd.h>

// Ensure kill prototype is visible on all platforms
extern int kill(pid_t, int);

// Static variable to hold the log file pointer
static FILE *s_log_file = NULL;

// Set the FILE* used for logging. Call this once after opening the log file.
void set_log_file(FILE *f) {
    s_log_file = f;
}

// Log a textual event (written to the log file if set).
void log_event(const char *msg) {
    if (!s_log_file) return;
    fprintf(s_log_file, "%s\n", msg);
    fflush(s_log_file);
}

// Send a signal to a pid and log success/failure.
void safe_kill(pid_t pid, int sig, const char *desc) {
    if (kill(pid, sig) < 0) {
        char buf[256];
        snprintf(buf, sizeof(buf), "[Parent] kill(%d,%d) failed for %s: %s",
                 (int)pid, sig, desc, strerror(errno));
        log_event(buf);
    } else {
        char buf[128];
        snprintf(buf, sizeof(buf), "[Parent] Sent signal %d to pid=%d (%s)",
                 sig, (int)pid, desc);
        log_event(buf);
    }
}
