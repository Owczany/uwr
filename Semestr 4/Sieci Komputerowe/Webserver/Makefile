# Nazwa pliku wykonywalnego
TARGET = webserver

# Kompilator
CC = gcc

# Flagi kompilatora
CFLAGS = -Wall -Wextra -std=c11 -O2

# Pliki źródłowe i obiektowe
SRCS = webserver.c server.c
OBJS = $(SRCS:.c=.o)

# Domyślny cel
all: $(TARGET)

# Kompilacja pliku wynikowego
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Reguła dla plików .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Czyszczenie clean
clean:
	rm -f $(OBJS) $(TARGET)

# Czyszczenie distclean
distclean: clean
	rm -f $(TARGET)