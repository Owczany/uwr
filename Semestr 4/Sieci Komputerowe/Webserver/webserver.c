// Piotr Pijanowski 346952

#include "server.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/stat.h>

#define BACKLOG 10     // Maksymalna liczba oczekujących połączeń

void usage(const char *progname)
{
    fprintf(stderr, "Użycie: %s <port> <katalog>\n", progname);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
    if (argc != 3) usage(argv[0]);

    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Niepoprawny numer portu: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    const char *web_root = argv[2];
    struct stat st;
    if (stat(web_root, &st) != 0 || !S_ISDIR(st.st_mode)) {
        fprintf(stderr, "Katalog nie istnieje lub nie jest katalogiem: %s\n", web_root);
        exit(EXIT_FAILURE);
    }

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket"); exit(EXIT_FAILURE); }

    int optval = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, BACKLOG) < 0) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Serwer nasłuchuje na porcie %d, katalog: %s\n", port, web_root);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        handle_client(client_fd, web_root);
    }

    close(server_fd);
    return 0;
}
