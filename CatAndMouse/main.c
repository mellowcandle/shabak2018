#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

void pabort(const char *str)
{
	perror(str);
	abort();
}
int main ()
{
	int fd,rc;
	uint8_t type;
	uint32_t length;
	uint8_t value[1024];
	uint32_t timestamp;
	uint32_t date;
	uint32_t multiplier = 75;
	uint32_t new_multiplier = 0;
	struct tm tm;
	float latitude, longitude;
	time_t time;

	fd = open("./external_mem_dump.bin", O_RDONLY);
	if (fd == -1)
		pabort("Failed opening the file\n");

	while (1)
	{
		rc = read(fd, &type, 1);
		if (rc != 1)
			pabort("Failed reading type");
		rc = read(fd, &length, 4);
		if (rc != 4)
			pabort("Failed reading length");
		if (length) {
			rc = read(fd, value, length);
			if (rc != length)
				pabort("Failed reading value");
		}
		switch (type) {
		case 0:
			printf("------------Reset----------\n");
			timestamp = *((uint32_t *)value);
			date = *((uint32_t *) &value[4]);
			multiplier = 150;
			memset(&tm, 0, sizeof(tm));
			tm.tm_sec = timestamp % 100;
			timestamp /= 100;
			tm.tm_min = timestamp % 100;
			timestamp /= 100;
			tm.tm_hour = timestamp;
			tm.tm_year = (date % 100) + 100;
			date /= 100;
			tm.tm_mon = (date % 100) - 1;
			date /= 100;
			tm.tm_mday = date;
			time = mktime(&tm);
			break;
		case 1:
			latitude = *((float *)value);
			longitude = *((float *) &value[4]);
			printf("Latitude: %.5f, Longitude: %.5f %s", latitude, longitude,
			       ctime(&time));
			time += multiplier * 4;
			if (new_multiplier) {
				multiplier = new_multiplier;
				new_multiplier = 0;
			}
			break;
		case 2:
			new_multiplier = 15;
			break;
		case 3:
			new_multiplier = 150;
			break;
		default:
			printf("Unknown type\n");
			break;
		}
	}

	return 0;
}
