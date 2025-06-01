#include "server.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <limits.h>  // dla PATH_MAX

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

#define BUF_SIZE 8192            // Rozmiar bufora danych
#define KEEP_ALIVE_TIMEOUT 1     // Czas oczekiwania na kolejne żądanie (sekundy)

// Zwraca MIME-type na podstawie rozszerzenia pliku
const char *get_mime_type(const char *path)
{
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

// Wysyła odpowiedź HTTP z nagłówkiem i treścią (jeśli obecna)
void send_response(int client_fd, int status, const char *status_text, const char *content_type, const char *body, int keep_alive)
{
    char header[1024];
    int length = body ? (int)strlen(body) : 0;
    snprintf(header, sizeof(header),
             "HTTP/1.1 %d %s\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %d\r\n"
             "Connection: %s\r\n"
             "\r\n",
             status, status_text, content_type, length, keep_alive ? "keep-alive" : "close");

    if (send(client_fd, header, strlen(header), 0) < 0) perror("send");
    if (body && send(client_fd, body, length, 0) < 0) perror("send body");
}

// Wysyła zawartość pliku do klienta
void send_file(int client_fd, const char *path)
{
    int fd = open(path, O_RDONLY);
    if (fd < 0)
    {
        send_response(client_fd, 404, "Not Found", "text/html; charset=utf-8", "<h1>404 Not Found</h1>", 0);
        return;
    }

    struct stat st;
    if (fstat(fd, &st) != 0)
    {
        close(fd);
        send_response(client_fd, 500, "Internal Server Error", "text/html; charset=utf-8", "<h1>500 Internal Server Error</h1>", 0);
        return;
    }
    int size = st.st_size;
    const char *mime = get_mime_type(path);

    char header[1024];
    snprintf(header, sizeof(header),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %d\r\n"
             "Connection: keep-alive\r\n"
             "\r\n",
             mime, size);
    if (send(client_fd, header, strlen(header), 0) < 0) perror("send header");

    char buffer[4096];
    ssize_t n;
    while ((n = read(fd, buffer, sizeof(buffer))) > 0)
    {
        if (send(client_fd, buffer, n, 0) < 0)
        {
            perror("send file chunk");
            break;
        }
    }
    close(fd);
}

void handle_client(int client_fd, const char *base_dir) {
    char buffer[BUF_SIZE];
    char method[8], path[1024], protocol[16];
    char hostname[256];
    char domain_dir[PATH_MAX];
    char fullpath[PATH_MAX];
    char real_fullpath[PATH_MAX];
    char real_base[PATH_MAX];

    struct timeval timeout;
    timeout.tv_sec = KEEP_ALIVE_TIMEOUT;
    timeout.tv_usec = 0;

    while (1) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(client_fd, &fds);

        int ready = select(client_fd + 1, &fds, NULL, NULL, &timeout);
        if (ready <= 0) break;

        ssize_t received = recv(client_fd, buffer, BUF_SIZE - 1, 0);
        if (received <= 0) break;

        buffer[received] = '\0';
        printf("DEBUG: Otrzymano zapytanie:\n%s\n", buffer);

        if (sscanf(buffer, "%7s %1023s %15s", method, path, protocol) != 3) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Not Implemented</h1>", 0);
            break;
        }

        if (strcmp(method, "GET") != 0) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Not Implemented</h1>", 0);
            break;
        }

        char *host = strstr(buffer, "\nHost:");
        if (!host) host = strstr(buffer, "\nhost:");
        if (!host) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Host header missing</h1>", 0);
            break;
        }
        host += 6;
        while (*host == ' ') host++;
        sscanf(host, "%255[^:\r\n]", hostname);

        snprintf(domain_dir, sizeof(domain_dir), "%s/%s", base_dir, hostname);
        snprintf(fullpath, sizeof(fullpath), "%s%s", domain_dir, path);

        struct stat st;
        if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {
            char location[1024];
            if (strlen(path) < 900) {
                if (path[strlen(path) - 1] != '/')
                    snprintf(location, sizeof(location), "HTTP/1.1 301 Moved Permanently\r\nLocation: %s/index.html\r\nConnection: keep-alive\r\n\r\n", path);
                else
                    snprintf(location, sizeof(location), "HTTP/1.1 301 Moved Permanently\r\nLocation: %sindex.html\r\nConnection: keep-alive\r\n\r\n", path);
                send(client_fd, location, strlen(location), 0);
            } else {
                send_response(client_fd, 414, "Request-URI Too Long", "text/html; charset=utf-8", "<h1>414 URI Too Long</h1>", 0);
            }
            continue;
        }

        if (!realpath(domain_dir, real_base)) {
            send_response(client_fd, 500, "Internal Server Error", "text/html; charset=utf-8", "<h1>500 Internal Server Error</h1>", 0);
            continue;
        }
        if (!realpath(fullpath, real_fullpath)) {
            send_response(client_fd, 404, "Not Found", "text/html; charset=utf-8", "<h1>404 Not Found</h1>", 0);
            continue;
        }

        if (strncmp(real_fullpath, real_base, strlen(real_base)) != 0) {
            send_response(client_fd, 403, "Forbidden", "text/html; charset=utf-8", "<h1>403 Forbidden</h1>", 0);
            continue;
        }

        send_file(client_fd, real_fullpath);

        if (strstr(buffer, "Connection: close") || strstr(buffer, "connection: close")) {
            break;
        }

        timeout.tv_sec = KEEP_ALIVE_TIMEOUT;
        timeout.tv_usec = 0;
    }

    close(client_fd);
}
