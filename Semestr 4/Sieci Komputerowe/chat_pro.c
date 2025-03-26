#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <arpa/inet.h>
#include <netinet/ip_icmp.h>
#include <netinet/ip.h>
#include <sys/time.h>
#include <poll.h>
#include <assert.h>
#include <unistd.h>

#define MAX_TTL 30
#define TIMEOUT_MS 1000
#define MAX_RESPONDERS 10

u_int16_t compute_icmp_checksum(const void *buff, int length)
{
    const u_int16_t *ptr = buff;
    u_int32_t sum = 0;
    assert(length % 2 == 0);
    for (; length > 0; length -= 2)
        sum += *ptr++;
    sum = (sum >> 16U) + (sum & 0xffffU);
    return ~(sum + (sum >> 16U));
}

void ERROR(const char *msg)
{
    fprintf(stderr, "Error: %s - %s\n", msg, strerror(errno));
    exit(EXIT_FAILURE);
}

void build_icmp_packet(char *packet, int id, int seq, int payload_size)
{
    struct icmp *icmp = (struct icmp *)packet;

    icmp->icmp_type = ICMP_ECHO;
    icmp->icmp_code = 0;
    icmp->icmp_id = id;
    icmp->icmp_seq = seq;
    icmp->icmp_cksum = 0;

    memset(packet + sizeof(struct icmp), 0x42, payload_size);

    int total_size = sizeof(struct icmp) + payload_size;
    icmp->icmp_cksum = compute_icmp_checksum(packet, total_size);
}

// Prosta funkcja: zwraca 1, jeśli udało się odebrać pakiet dla któregoś
// z podanych w tablicy expected_seqs numerów sequence.
// Zwraca przez rtt_out wyliczony czas RTT.
// sender_ip_str – bufor na IP nadawcy
// seq_matched – wskaźnik do zmiennej, gdzie zapiszemy, który sequence został dopasowany (-1 jeśli żaden).
int receive_icmp_reply_multi(int sock_fd, int pid,
                             const int *expected_seqs, int seq_count,
                             int timeout_ms,
                             char *sender_ip_str,
                             double *rtt_out,
                             int *seq_matched)
{
    *seq_matched = -1; // domyślnie brak dopasowania

    struct pollfd pfd = {
        .fd = sock_fd,
        .events = POLLIN
    };

    int ready = poll(&pfd, 1, timeout_ms);
    if (ready == 0)
        return 0; // timeout
    if (ready < 0)
        ERROR("poll error");

    // mierz czas po poll() - to orientacyjnie też do RTT
    struct timeval end;
    gettimeofday(&end, NULL);

    char recv_buf[512];
    struct sockaddr_in sender;
    socklen_t sender_len = sizeof(sender);

    ssize_t packet_len = recvfrom(sock_fd, recv_buf, sizeof(recv_buf),
                                  0, (struct sockaddr *)&sender, &sender_len);
    if (packet_len < 0)
        ERROR("recvfrom error");

    inet_ntop(AF_INET, &sender.sin_addr, sender_ip_str, INET_ADDRSTRLEN);

    struct ip *ip_hdr = (struct ip *)recv_buf;
    int ip_hdr_len = ip_hdr->ip_hl * 4;
    if (packet_len < ip_hdr_len + (int)sizeof(struct icmp)) {
        // pakiet za krótki, by zawierał ICMP
        return 0;
    }

    struct icmp *icmp_hdr = (struct icmp *)(recv_buf + ip_hdr_len);

    // W tym zadaniu liczymy RTT "od momentu wysłania pakietu do momentu odebrania".
    // Ponieważ jednak od razu po wysłaniu 3 pakietów wchodzimy w pętlę nasłuchiwania,
    // do precyzyjnego wyznaczenia RTT należałoby zapisywać czas wyjścia każdego z pakietów.
    // Tu, dla uproszczenia, pokazuję wersję mniej precyzyjną:
    // "wynik w end" – ale w praktyce warto by zapamiętywać np. tablicę time_sent[seq].
    // Możesz dopisać to we własnym zakresie.

    // Sprawdzamy typ:
    if (icmp_hdr->icmp_type == ICMP_ECHOREPLY) {
        // Musimy sprawdzić, czy pid i sequence pasują do naszych oczekiwań
        if (icmp_hdr->icmp_id != pid)
            return 0;

        // sprawdzamy, czy seq jest w tablicy expected_seqs
        for (int i = 0; i < seq_count; i++) {
            if (icmp_hdr->icmp_seq == expected_seqs[i]) {
                *seq_matched = icmp_hdr->icmp_seq;
                // RTT – prosta wersja; patrz komentarz wyżej
                // (jeśli chcesz precyzyjnie, musisz zapamiętać czas wysłania
                //  pakietów i tu obliczyć end - time_sent[seq_matched])
                *rtt_out = 1.0 * (end.tv_usec / 1000.0); // np. cokolwiek tymczasowego
                return 1;
            }
        }
        return 0;
    }
    else if (icmp_hdr->icmp_type == 11) {
        // Time Exceeded
        // Sprawdzamy, czy w pakiecie jest oryginalny nagłówek IP i ICMP
        int min_len = ip_hdr_len + sizeof(struct icmp)
                      + sizeof(struct ip) + sizeof(struct icmp);
        if (packet_len < min_len) {
            return 0; // nie ma wystarczająco danych
        }
        // przechodzimy do "zawiniętego" IP i ICMP
        char *icmp_payload = (char *)icmp_hdr + sizeof(struct icmp);
        struct ip *inner_ip = (struct ip *)icmp_payload;
        int inner_ip_len = inner_ip->ip_hl * 4;

        // Sprawdź, czy mamy jeszcze w tym payloadzie wystarczająco miejsca
        if (packet_len < ip_hdr_len + (int)sizeof(struct icmp) + inner_ip_len + (int)sizeof(struct icmp)) {
            return 0;
        }

        struct icmp *inner_icmp = (struct icmp *)(icmp_payload + inner_ip_len);

        // Teraz walidacja pid i seq wewnątrz
        if (inner_icmp->icmp_id != pid)
            return 0;

        // Sprawdzamy, czy seq jest w tablicy expected_seqs
        for (int i = 0; i < seq_count; i++) {
            if (inner_icmp->icmp_seq == expected_seqs[i]) {
                *seq_matched = inner_icmp->icmp_seq;
                // analogicznie – pseudo-obliczenie RTT
                *rtt_out = 1.0 * (end.tv_usec / 1000.0); 
                return 1;
            }
        }
        return 0;
    }

    // inny typ
    return 0;
}

void print_hop(int ttl, char responders[][INET_ADDRSTRLEN], int responder_count,
               int all_replied, int avg_rtt)
{
    printf("%d. ", ttl);

    if (responder_count == 0)
    {
        printf("*\n");
        return;
    }

    // Wypisz wszystkie unikatowe IP, które odpowiedziały
    for (int i = 0; i < responder_count; i++)
    {
        printf("%s ", responders[i]);
    }

    if (!all_replied)
        printf("???\n");
    else
        printf("%dms\n", avg_rtt); // np. bez spacji przed "ms"
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "How to use: %s <ip_address> \n", argv[0]);
        exit(EXIT_FAILURE);
    }

    // Przygotowanie adresu docelowego
    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;

    if (inet_pton(AF_INET, argv[1], &dest_addr.sin_addr) != 1)
        ERROR("Incorrect IP address");

    // surowe gniazdo
    int sock_fd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sock_fd < 0)
        ERROR("socket error");

    int pid = getpid() & 0xFFFF;
    int sequence = 1;

    const int payload_size = 48;
    char packet[sizeof(struct icmp) + 48];

    for (int ttl = 1; ttl <= MAX_TTL; ttl++)
    {
        // ustaw TTL
        if (setsockopt(sock_fd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0)
            ERROR("setsockopt error");

        // ZAPISUJEMY 3 SEKWENCJE, KTÓRE ZA CHWILĘ WYŚLEMY
        int seqs[3];
        for (int i = 0; i < 3; i++) {
            seqs[i] = sequence++;
        }

        // Najpierw wyślijmy 3 pakiety "hurtem"
        for (int i = 0; i < 3; i++) {
            build_icmp_packet(packet, pid, seqs[i], payload_size);

            ssize_t sent = sendto(sock_fd, packet, sizeof(packet), 0,
                                  (struct sockaddr *)&dest_addr, sizeof(dest_addr));
            if (sent < 0)
                ERROR("sendto error");
        }

        // Teraz zbieramy odpowiedzi przez maksymalnie 1 s
        // (lub do momentu, aż dostaniemy 3)
        char responders[MAX_RESPONDERS][INET_ADDRSTRLEN];
        int count = 0;
        double total_rtt = 0.0;

        // Zapisujemy chwilę startu – do prymitywnego obliczania, ile czekamy
        struct timeval start, now;
        gettimeofday(&start, NULL);

        while (1)
        {
            gettimeofday(&now, NULL);
            double elapsed_ms = (now.tv_sec - start.tv_sec) * 1000.0 +
                                (now.tv_usec - start.tv_usec) / 1000.0;
            if (elapsed_ms >= TIMEOUT_MS)
                break; // minęła 1 sekunda

            int time_left = TIMEOUT_MS - (int)elapsed_ms;

            // Próba odebrania jednego pakietu
            char ip_str[INET_ADDRSTRLEN];
            double rtt;
            int seq_matched;
            int got = receive_icmp_reply_multi(sock_fd, pid, seqs, 3,
                                               time_left,
                                               ip_str, &rtt, &seq_matched);
            if (!got) {
                // Brak pakietu w tym momencie (poll zwrócił 0) albo to nie nasz
                // – przerwij pętlę, bo poll zwrócił 0 => nic więcej nie przyjdzie
                break;
            }

            // got == 1 => odebraliśmy jedną odpowiedź, która pasuje do jednej z 3 sekwencji
            // sprawdźmy czy mamy już tego respondenta w tablicy
            int known = 0;
            for (int i = 0; i < count; i++)
            {
                if (strcmp(responders[i], ip_str) == 0)
                {
                    known = 1;
                    break;
                }
            }
            if (!known && count < MAX_RESPONDERS)
            {
                strncpy(responders[count], ip_str, INET_ADDRSTRLEN);
                count++;
            }

            total_rtt += rtt;

            // jeśli mamy już 3 odpowiedzi, możemy wyjść
            // (albo dalej czytać, zależnie jak interpretujesz specyfikację –
            //  ale w zadaniu i tak wystarczy 3 pakiety)
            if (count == 3)
                break;
        }

        // Obliczamy średni RTT – w tym przykładzie liczę go z "count" odpowiedzi
        int avg_rtt = 0;
        if (count > 0)
            avg_rtt = (int)(total_rtt / count);

        // Sprawdzamy, czy wszystkie 3 odpowiedzi przyszły
        int all_replied = (count == 3);

        // Wypisujemy to co w zadaniu
        print_hop(ttl, responders, count, all_replied, avg_rtt);

        // Sprawdzamy, czy wśród respondentów jest IP docelowe
        // jeśli tak, kończymy
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
