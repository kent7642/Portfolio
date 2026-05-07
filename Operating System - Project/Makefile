CC=gcc
CFLAGS=-Wall -Wextra -std=c11
LDFLAGS=-lm
SOURCES=main.c scheduler.c process.c scheduler_utils.c
TARGET=scheduler

.PHONY: all clean run test

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) $(LDFLAGS) -o $(TARGET)

run: all
	./$(TARGET) 4 100 scheduler.log

# Run for 5 seconds to smoke-test the scheduler (requires `timeout`)
test: all
	timeout 5s ./$(TARGET) 4 100 scheduler.log || true

clean:
	rm -f $(TARGET) *.o scheduler.log
