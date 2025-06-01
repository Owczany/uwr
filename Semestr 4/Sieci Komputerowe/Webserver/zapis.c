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
#include <time.h>
#include <sys/select.h>

#define BACKLOG 10
#define BUF_SIZE 8192
#define KEEP_ALIVE_TIMEOUT 1 // sekunda

// Wypisuje instrukcję użycia programu
void usage(const char *progname)
{
    fprintf(stderr, "U\u017cycie: %s <port> <katalog>\n", progname);
    exit(EXIT_FAILURE);
}

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

// Wysyła odpowiedź HTTP z treścią body (lub bez)
void send_response(int client_fd, int status, const char *status_text, const char *content_type, const char *body)
{
    char header[1024];
    int length = body ? strlen(body) : 0;
    snprintf(header, sizeof(header),
             "HTTP/1.1 %d %s\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %d\r\n"
             "Connection: close\r\n"
             "\r\n",
             status, status_text, content_type, length);

    if (send(client_fd, header, strlen(header), 0) < 0) perror("send");
    if (body && send(client_fd, body, length, 0) < 0) perror("send body");
}

// Wysyła zawartość pliku
void send_file(int client_fd, const char *path)
{
    int fd = open(path, O_RDONLY);
    if (fd < 0)
    {
        send_response(client_fd, 404, "Not Found", "text/html; charset=utf-8", "<h1>404 Not Found</h1>");
        return;
    }

    struct stat st;
    if (fstat(fd, &st) != 0)
    {
        close(fd);
        send_response(client_fd, 500, "Internal Server Error", "text/html; charset=utf-8", "<h1>500 Internal Server Error</h1>");
        return;
    }
    int size = st.st_size;
    const char *mime = get_mime_type(path);

    char header[1024];
    snprintf(header, sizeof(header),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %d\r\n"
             "Connection: close\r\n"
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

// Obsługuje pojedyncze zapytanie klienta


void handle_client(int client_fd, const char *base_dir) {
    char buffer[BUF_SIZE];
    char method[8], path[1024], protocol[16];
    char hostname[256];
    char fullpath[2048];
    char real_fullpath[2048];
    char real_base[2048];

    // Timeout w sekundach
    struct timeval timeout;
    timeout.tv_sec = 1;
    timeout.tv_usec = 0;

    realpath(base_dir, real_base);

    while (1) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(client_fd, &fds);

        int ready = select(client_fd + 1, &fds, NULL, NULL, &timeout);
        if (ready <= 0) break; // timeout lub błąd

        ssize_t received = recv(client_fd, buffer, BUF_SIZE - 1, 0);
        if (received <= 0) break; // klient zamknął połączenie

        buffer[received] = '\0';
        printf("DEBUG: Otrzymano zapytanie:\n%s\n", buffer);

        if (sscanf(buffer, "%7s %1023s %15s", method, path, protocol) != 3) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                          "<h1>501 Not Implemented</h1>");
            break;
        }

        if (strcmp(method, "GET") != 0) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                          "<h1>501 Not Implemented</h1>");
            break;
        }

        char *host = strstr(buffer, "\nHost:");
        if (!host) host = strstr(buffer, "\nhost:");
        if (!host) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8",
                          "<h1>501 Host header missing</h1>");
            break;
        }
        host += 6;
        while (*host == ' ') host++;
        sscanf(host, "%255[^:\r\n]", hostname);

        snprintf(fullpath, sizeof(fullpath), "%s/%s%s", base_dir, hostname, path);

        struct stat st;
        if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {
            char location[1024];
            if (path[strlen(path) - 1] != '/')
                snprintf(location, sizeof(location),
                         "HTTP/1.1 301 Moved Permanently\r\nLocation: %s/index.html\r\n\r\n", path);
            else
                snprintf(location, sizeof(location),
                         "HTTP/1.1 301 Moved Permanently\r\nLocation: %sindex.html\r\n\r\n", path);
            send(client_fd, location, strlen(location), 0);
            continue;
        }

        realpath(fullpath, real_fullpath);
        printf("DEBUG: fullpath = %s\n", real_fullpath);
        printf("DEBUG: base_dir = %s\n", real_base);
        if (strncmp(real_fullpath, real_base, strlen(real_base)) != 0) {
            send_response(client_fd, 403, "Forbidden", "text/html; charset=utf-8",
                          "<h1>403 Forbidden</h1>");
            continue;
        }

        send_file(client_fd, real_fullpath);

        // Jeżeli nagłówek zawiera "Connection: close", zakończ pętlę
        if (strstr(buffer, "Connection: close") || strstr(buffer, "connection: close")) {
            break;
        }

        // Reset timeout dla kolejnego zapytania
        timeout.tv_sec = 1;
        timeout.tv_usec = 0;
    }

    close(client_fd);
}

int main(int argc, char *argv[])
{
    if (argc != 3) usage(argv[0]);

    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535)
    {
        fprintf(stderr, "Niepoprawny numer portu: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    const char *web_root = argv[2];
    struct stat st;
    if (stat(web_root, &st) != 0 || !S_ISDIR(st.st_mode))
    {
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

    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, BACKLOG) < 0)
    {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Serwer nasłuchuje na porcie %d, katalog: %s\n", port, web_root);

    while (1)
    {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0)
        {
            perror("accept");
            continue;
        }

        handle_client(client_fd, web_root);
    }

    close(server_fd);
    return 0;
}
