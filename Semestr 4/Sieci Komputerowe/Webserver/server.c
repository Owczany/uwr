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

// Wysyła zawartość pliku do klienta
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

    // Wysyłanie nagłówka HTTP
    char header[1024];
    snprintf(header, sizeof(header),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: %s\r\n"
             "Content-Length: %d\r\n"
             "Connection: close\r\n"
             "\r\n",
             mime, size);
    if (send(client_fd, header, strlen(header), 0) < 0) perror("send header");

    // Wysyłanie zawartości pliku
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

// Obsługuje pojedynczego klienta (obsługa wielu zapytań w jednym połączeniu)
void handle_client(int client_fd, const char *base_dir) {
    char buffer[BUF_SIZE];
    char method[8], path[1024], protocol[16];
    char hostname[256];
    char domain_dir[2048];
    char fullpath[2048];
    char real_fullpath[2048];
    char real_base[2048];

    // Ustawienie timeoutu keep-alive
    struct timeval timeout;
    timeout.tv_sec = KEEP_ALIVE_TIMEOUT;
    timeout.tv_usec = 0;

    while (1) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(client_fd, &fds);

        // Czekaj na dane od klienta z timeoutem
        int ready = select(client_fd + 1, &fds, NULL, NULL, &timeout);
        if (ready <= 0) break;

        // Odbierz dane
        ssize_t received = recv(client_fd, buffer, BUF_SIZE - 1, 0);
        if (received <= 0) break;

        buffer[received] = '\0';
        printf("DEBUG: Otrzymano zapytanie:\n%s\n", buffer);

        // Parsowanie linii żądania (metoda, ścieżka, protokół)
        if (sscanf(buffer, "%7s %1023s %15s", method, path, protocol) != 3) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Not Implemented</h1>");
            break;
        }

        // Obsługiwane tylko zapytania GET
        if (strcmp(method, "GET") != 0) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Not Implemented</h1>");
            break;
        }

        // Odczytanie nagłówka Host
        char *host = strstr(buffer, "\nHost:");
        if (!host) host = strstr(buffer, "\nhost:");
        if (!host) {
            send_response(client_fd, 501, "Not Implemented", "text/html; charset=utf-8", "<h1>501 Host header missing</h1>");
            break;
        }
        host += 6;
        while (*host == ' ') host++;
        sscanf(host, "%255[^:\r\n]", hostname);

        // Zbudowanie ścieżki do zasobu
        snprintf(domain_dir, sizeof(domain_dir), "%s/%s", base_dir, hostname);
        snprintf(fullpath, sizeof(fullpath), "%s%s", domain_dir, path);

        // Obsługa przekierowania z katalogu (dodanie /index.html)
        struct stat st;
        if (stat(fullpath, &st) == 0 && S_ISDIR(st.st_mode)) {
            char location[1024];
            if (path[strlen(path) - 1] != '/')
                snprintf(location, sizeof(location), "HTTP/1.1 301 Moved Permanently\r\nLocation: %s/index.html\r\n\r\n", path);
            else
                snprintf(location, sizeof(location), "HTTP/1.1 301 Moved Permanently\r\nLocation: %sindex.html\r\n\r\n", path);
            send(client_fd, location, strlen(location), 0);
            continue;
        }

        // Sprawdzenie ścieżki rzeczywistej (ochrona przed ../)
        realpath(domain_dir, real_base);
        realpath(fullpath, real_fullpath);
        printf("DEBUG: fullpath = %s\n", real_fullpath);
        printf("DEBUG: base_dir = %s\n", real_base);

        if (strncmp(real_fullpath, real_base, strlen(real_base)) != 0) {
            send_response(client_fd, 403, "Forbidden", "text/html; charset=utf-8", "<h1>403 Forbidden</h1>");
            continue;
        }

        // Wysyłanie pliku
        send_file(client_fd, real_fullpath);

        // Sprawdzenie nagłówka Connection
        if (strstr(buffer, "Connection: close") || strstr(buffer, "connection: close")) {
            break;
        }

        // Reset timeoutu
        timeout.tv_sec = KEEP_ALIVE_TIMEOUT;
        timeout.tv_usec = 0;
    }

    close(client_fd);
}
