#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
	FILE *ptr;
	char a;
	char filename[50];
	printf("Enter the name of file you wish to open: ");
	scanf("%s",filename);
	ptr = fopen(filename, "r");

	if (NULL == ptr) 
	{
		printf("file can't be opened \n");
	}

	printf("content of this file are \n");

	do {
		a = fgetc(ptr);
		printf("%c", a);
	} while (a != EOF);
	fclose(ptr);
	return 0;
}

