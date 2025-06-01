#ifndef SERVER_H
#define SERVER_H

void handle_client(int client_fd, const char *base_dir);
const char *get_mime_type(const char *path);
void send_response(int client_fd, int status, const char *status_text, const char *content_type, const char *body, int keep_alive);
void send_file(int client_fd, const char *path);

#endif
