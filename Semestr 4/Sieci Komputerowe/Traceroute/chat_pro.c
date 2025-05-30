// Piotr Pijanowski 346952 - macOS version

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <sys/time.h>
#include <poll.h>
#include <unistd.h>
#include <assert.h>
#include <sys/socket.h>

#define PAYLOAD_SIZE 48
#define MAX_TTL 30
#define MAX_RESPONDERS 10
#define TIMEOUT_MS 1000

// Checksum function
uint16_t compute_icmp_checksum(const void *buff, int length)
{
    const uint16_t *ptr = buff;
    uint32_t sum = 0;
    assert(length % 2 == 0);
    for (; length > 0; length -= 2)
        sum += *ptr++;
    sum = (sum >> 16U) + (sum & 0xffffU);
    return ~(sum + (sum >> 16U));
}

void build_icmp_packet(char *packet, int id, int seq, int payload_size)
{
    struct icmp *icmp_hdr = (struct icmp *)packet;

    icmp_hdr->icmp_type = ICMP_ECHO;
    icmp_hdr->icmp_code = 0;
    icmp_hdr->icmp_id = id;
    icmp_hdr->icmp_seq = seq;
    memset(packet + sizeof(struct icmp), 0x42, payload_size);

    int total_size = sizeof(struct icmp) + payload_size;
    icmp_hdr->icmp_cksum = 0;
    icmp_hdr->icmp_cksum = compute_icmp_checksum(packet, total_size);
}

void ERROR(const char *msg)
{
    fprintf(stderr, "Error: %s - %s\n", msg, strerror(errno));
    exit(EXIT_FAILURE);
}

void print_hop(int ttl, char responders[][INET_ADDRSTRLEN], int responder_count, int all_replied, double avg_rtt)
{
    printf("%d. ", ttl);

    if (responder_count == 0)
    {
        printf("*\n");
        return;
    }

    for (int i = 0; i < responder_count; i++)
    {
        printf("%s ", responders[i]);
    }

    if (!all_replied)
        printf("???\n");
    else
        printf("%.2fms\n", avg_rtt);
}

int receive_icmp_reply(int sock_fd, int pid, int expected_seq, int timeout_ms,
                       char *sender_ip_str, double *rtt)
{
    struct pollfd pfd = {.fd = sock_fd, .events = POLLIN};

    struct timeval start, end;
    gettimeofday(&start, NULL);

    int timeout = poll(&pfd, 1, timeout_ms);
    if (timeout == 0)
        return 0;
    if (timeout < 0)
        ERROR("poll error");

    char recv_buf[IP_MAXPACKET];
    struct sockaddr_in sender;
    socklen_t sender_len = sizeof(sender);

    ssize_t packet_len = recvfrom(sock_fd, recv_buf, IP_MAXPACKET, 0, (struct sockaddr *)&sender, &sender_len);
    if (packet_len < 0)
        ERROR("recvfrom error");

    gettimeofday(&end, NULL);
    inet_ntop(AF_INET, &sender.sin_addr, sender_ip_str, INET_ADDRSTRLEN);

    struct ip *ip_hdr = (struct ip *)recv_buf;
    int ip_hdr_len = ip_hdr->ip_hl * 4;

    struct icmp *icmp_hdr = (struct icmp *)(recv_buf + ip_hdr_len);

    if (icmp_hdr->icmp_type == ICMP_ECHOREPLY)
    {
        if (icmp_hdr->icmp_id != pid || icmp_hdr->icmp_seq != expected_seq)
            return 0;

        *rtt = (end.tv_sec - start.tv_sec) * 1000.0 +
               (end.tv_usec - start.tv_usec) / 1000.0;
        return 1;
    }
    else if (icmp_hdr->icmp_type == 11)
    {
        struct ip *inner_ip = (struct ip *)(recv_buf + ip_hdr_len + sizeof(struct icmp));
        int inner_ip_len = inner_ip->ip_hl * 4;
        struct icmp *inner_icmp = (struct icmp *)((char *)inner_ip + inner_ip_len);

        if (inner_icmp->icmp_id != pid || inner_icmp->icmp_seq != expected_seq)
            return 0;

        *rtt = (end.tv_sec - start.tv_sec) * 1000.0 +
               (end.tv_usec - start.tv_usec) / 1000.0;
        return 1;
    }

    return 0;
}

int main(int argc, char const *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "HOW TO USE: %s <ip_address>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;

    if (inet_pton(AF_INET, argv[1], &dest_addr.sin_addr) != 1)
        ERROR("Incorrect IP address");

    int sock_fd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sock_fd < 0)
        ERROR("Creating raw socket");

    int pid = getpid() & 0xFFFF;
    int sequence = 1;
    char packet[sizeof(struct icmp) + PAYLOAD_SIZE];

    for (int ttl = 1; ttl <= MAX_TTL; ttl++)
    {
        if (setsockopt(sock_fd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0)
            ERROR("setsockopt");

        char responders[MAX_RESPONDERS][INET_ADDRSTRLEN];
        int count = 0;
        int distinct_responder_count = 0;
        double total_rtt = 0;

        for (int i = 0; i < 3; i++)
        {
            build_icmp_packet(packet, pid, sequence, PAYLOAD_SIZE);
            ssize_t sent = sendto(sock_fd, packet, sizeof(packet), 0,
                                  (struct sockaddr *)&dest_addr, sizeof(dest_addr));
            if (sent < 0)
                ERROR("sendto error");

            char ip[INET_ADDRSTRLEN];
            double rtt;
            if (receive_icmp_reply(sock_fd, pid, sequence, TIMEOUT_MS, ip, &rtt))
            {
                int already_present = 0;
                for (int j = 0; j < count; j++)
                {
                    if (strcmp(responders[j], ip) == 0)
                    {
                        already_present = 1;
                        break;
                    }
                }

                if (!already_present && distinct_responder_count < MAX_RESPONDERS)
                {
                    distinct_responder_count++;
                    strncpy(responders[count], ip, INET_ADDRSTRLEN);
                }
                total_rtt += rtt;
                count++;
            }

            sequence++;
        }

        double avg_rtt = (count > 0) ? (total_rtt / count) : 0;
        print_hop(ttl, responders, count, count == 3, avg_rtt);

        for (int i = 0; i < count; i++)
        {
            if (strcmp(responders[i], argv[1]) == 0)
            {
                close(sock_fd);
                return 0;
            }
        }
    }

    close(sock_fd);
    return 0;
}
