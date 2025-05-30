// Autor: jan_kowalski, 123456
// Plik: main.c

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

#define BACKLOG 10
#define BUF_SIZE 8192

void usage(const char *progname) {
    fprintf(stderr, "Użycie: %s <port> <katalog>\n", progname);
    exit(EXIT_FAILURE);
}

const char* get_mime_type(const char* path) {
    const char *dot = strrchr(path, '.');
    if (!dot) return "application/octet-stream";
    if (strcmp(dot, ".html") == 0) return "text/html; charset=utf-8";
    if (strcmp(dot, ".css") == 0) return "text/css; charset=utf-8";
    if (strcmp(dot, ".txt") == 0) return "text/plain; charset=utf-8";
    if (strcmp(dot, ".jpg") == 0 || strcmp(dot, ".jpeg") == 0) return "image/jpeg";
    if (strcmp(dot, ".png") == 0) return "image/png";
    if (strcmp(dot, ".pdf") == 0) return "application/pdf";
    return "application/octet-stream";
}

void send_response(int client_fd, int status, const char* status_text, const char* content_type, const char* body) {
    char header[1024];
    int length = body ? strlen(body) : 0;
    snprintf(header, sizeof(header),
        "HTTP/1.1 %d %s\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n",
        status, status_text, content_type, length);
    
    send(client_fd, header, strlen(header), 0);
    if (body) {
        send(client_fd, body, length, 0);
    }
}

void send_file(int client_fd, const char* path) {
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        send_response(client_fd, 404, "Not Found", "text/html; charset=utf-8",
                      "<h1>404 Not Found</h1>");
        return;
    }

    struct stat st;
    fstat(fd, &st);
    int size = st.st_size;
    const char* mime = get_mime_type(path);

    char header[1024];
    snprintf(header, sizeof(header),
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n", mime, size);
    send(client_fd, header, strlen(header), 0);

    char buffer[4096];
    ssize_t n;
    while ((n = read(fd, buffer, sizeof(buffer))) > 0) {
        send(client_fd, buffer, n, 0);
    }
    close(fd);
}

void handle_client(int client_fd, const char* base_dir) {
    char buffer[BUF_SIZE];
    ssize_t received = recv(client_fd, buffer, BUF_SIZE - 1, 0);
    if (received <= 0) {
        close(client_fd);
        return;
    }

    buffer[received] = '\0';

    // Parsuj pierwszą linię
    char method[8], path[1024], protocol[16];
    if (sscanf(buffer, "%7s %1023s %15s", method, path, protocol) != 3) {
        send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                      "<h1>501 Not Implemented</h1>");
        close(client_fd);
        return;
    }

    if (strcmp(method, "GET") != 0) {
        send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                      "<h1>501 Not Implemented</h1>");
        close(client_fd);
        return;
    }

    // Znajdź nagłówek Host
    char *host = strstr(buffer, "\nHost:");
    if (!host) host = strstr(buffer, "\nhost:");
    if (!host) {
        send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                      "<h1>501 Host header missing</h1>");
        close(client_fd);
        return;
    }
    host += 6; // pomiń 'Host:'
    while (*host == ' ') host++; // pomiń spacje
    char hostname[256];
    sscanf(host, "%255s", hostname);

    // Zbuduj pełną ścieżkę
    char fullpath[2048];
    snprintf(fullpath, sizeof(fullpath), "%s/%s%s", base_dir, hostname, path);

    // Sprawdź czy to katalog bez '/' na końcu – przekieruj do index.html
    struct stat st;
    if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {
        char location[1024];
        snprintf(location, sizeof(location), "HTTP/1.1 301 Moved Permanently\r\nLocation: %s/index.html\r\n\r\n", path);
        send(client_fd, location, strlen(location), 0);
        close(client_fd);
        return;
    }

    // Zabezpieczenie przed ../
    realpath(fullpath, fullpath); // canonical path
    char real_base[2048];
    realpath(base_dir, real_base);
    if (strncmp(fullpath, real_base, strlen(real_base)) != 0) {
        send_response(client_fd, 403, "Forbidden", "text/html; charset=utf-8",
                      "<h1>403 Forbidden</h1>");
        close(client_fd);
        return;
    }

    // Wysyłanie pliku
    send_file(client_fd, fullpath);
    close(client_fd);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        usage(argv[0]);
    }

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
    if (server_fd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    int optval = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
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
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        handle_client(client_fd, web_root);
    }

    close(server_fd);
    return 0;
}
