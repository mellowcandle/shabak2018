#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#define TRUE 1 
#define FALSE 0

#define PARSER_INVALID 0
#define PARSER_TYPE_1 1
#define PARSER_TYPE_2 2

#define PARSER_PREFIX_1 "GPGGA"
#define PARSER_PREFIX_2 "GPRMC"
#define PARSER_PREFIX_LENGTH 5
#define MAX_UART_BUFFER 256
#define DATA_MAX_LENGTH 100
#define DATA_MIN_LENGTH 9
#define MAX_SAVE_BUFFER_SIZE 256

uint8_t should_save = FALSE;
uint8_t reset = TRUE;
uint8_t counter = 0;
uint8_t counter_max_val = 75;
uint8_t is_triggered = FALSE;

static uint32_t uart_read(uint8_t *buffer){/* Read data from UART0 until 0x00 terminator */};

static uint8_t parse(uint8_t *in_buffer, uint32_t length, uint8_t **out_buffers)
{
    uint8_t i = 0;
    uint8_t res = PARSER_INVALID

    if (length < DATA_MIN_LENGTH || length > DATA_MAX_LENGTH || *in_buffer != '$' ||
        in_buffer[length - 1] != '\n' || in_buffer[6] != ',')
        return PARSER_INVALID;

    if (0 == strncmp(in_buffer + 1, PARSER_PREFIX_1, PARSER_PREFIX_LENGTH))
        res = PARSER_TYPE_1;
    else if (0 == strncmp(in_buffer + 1, PARSER_PREFIX_2, PARSER_PREFIX_LENGTH))
        res = PARSER_TYPE_2;
    else
        return PARSER_INVALID;

    in_buffer = in_buffer + PARSER_PREFIX_LENGTH + 2;

    out_buffers[i++] = in_buffer;
    while (NULL != (in_buffer = strchr(in_buffer, ',')))
    {
        *in_buffer = '\0';
        out_buffers[i++] = ++in_buffer;
    }

    return res;
}

static uint32_t format_save(uint8_t *in_buffer, uint8_t a, uint32_t length, uint8_t *out_buffer)
{
    *out_buffer = a;
    *(uint32_t *)&out_buffer[1] = length;
    memcpy(&out_buffer[5], in_buffer, length);
    return length + 5;
}

static uint32_t format1(uint8_t **in_buffer, uint8_t *out_buffer)
{
    *(int *)out_buffer = atoi(in_buffer[0]);
    out_buffer += sizeof(float);
    *(int *)out_buffer = atoi(in_buffer[8]);
    return 2 * sizeof(float);
}

static uint32_t format2(uint8_t **in_buffers, uint8_t *out_buffer)
{
    char val1_str[10] = { 0 };
    for (uint8_t i = 0; i < 3; i += 2)
    {
        memset(val1_str, 0, sizeof(val1_str));
        uint8_t *pos = strchr(in_buffers[i], '.');
        memcpy(val1_str, in_buffers[i], pos - in_buffers[i] - 2);
        uint16_t val1 = atoi(val1_str);
        float val2 = atof(pos - 2);
        float res =  val1 + (val2 / 60);
        if (*in_buffers[i + 1] == 'W' || *in_buffers[i + 1] == 'S')
            res *= -1;
        *(float *)out_buffer = res;
        out_buffer += sizeof(float);
    }
    return 2 * sizeof(float);
}

static void configure1(void)
{
    cli();
    should_save = FALSE;
    counter = 0;
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;
    OCR1A = 62499;
    TCCR1B |= (1 << WGM12);
    TCCR1B |= (1 << CS12) | (1 << CS10);
    TIMSK1 |= (1 << OCIE1A);
    sei();
}

static void configure2(void)
{
    cli();
    EICRA |= 0x01 << 2;
    EIMSK |= 0x01 << 2;
    sei();
}

ISR(TIMER1_COMPA_vect)
{
    if (++counter == counter_max_val)
    {
        should_save = TRUE;
        counter = 0;
        counter_max_val = (is_triggered == TRUE) ? 15 : 150;
    }
}

ISR(INT2_vect)
{
    static uint8_t interrupt_buffer[MAX_SAVE_BUFFER_SIZE];
    uint8_t *temp_buffer;
    uint8_t a;
    uint32_t length;
    if (PIND & 0x01)
    {
        is_triggered = TRUE;
        a = 2;
    }
    else
    {
        is_triggered = FALSE;
        a = 3;
    }

    length = format_save(temp_buffer, a, 0, interrupt_buffer);
    save_to_flash(interrupt_buffer, length);
}

static void save_to_flash(uint8_t *buffer, uint32_t length){ /* Save buffer to flash at next empty address */ }

static void configure_usart0(void) { /* Configure USART 0 */ }

static void configure_spi(void) { /* Configure SPI */ }

static void configure_two_wire_serial_interface(void) { /* Configure the two wire serial interface */ }

int main()
{
    uint32_t size = 0;
    uint8_t recv_buffer[MAX_UART_BUFFER];

    uint8_t *parsed_buffers[20];
    uint8_t save_buffer[MAX_SAVE_BUFFER_SIZE];
    uint8_t temp_buffer[MAX_SAVE_BUFFER_SIZE];
    uint32_t save_length = 0;
    uint8_t res;
    uint32_t formatted_length;
    uint8_t a = FALSE;

    configure_sysclk();	/* Assume system clock is 16 MHz */
    configure_usart0();
    configure_spi();
    configure_two_wire_serial_interface();
    configure1();
    configure2();

    while (1)
    {
        formatted_length = 0;
        size = uart_read(recv_buffer);

        if (size > 0)
        {
            res = parse(recv_buffer, size, parsed_buffers);
            if (reset == TRUE)
            {
                if(res != PARSER_TYPE_2) continue;

                formatted_length = format1(parsed_buffers, temp_buffer);

                reset = FALSE;
                a = TRUE;
            }
            else if (should_save == TRUE)
            {
                if(res != PARSER_TYPE_1) continue;

                formatted_length = format2(&parsed_buffers[1], temp_buffer);

                should_save = FALSE;

                a = FALSE;
            }

            if(formatted_length > 0)
            {
                save_length = format_save(temp_buffer, (a == TRUE) ? 0 : 1, formatted_length, save_buffer);
                save_to_flash(save_buffer, save_length);
            }
        }
    }
}

