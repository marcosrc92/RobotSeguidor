#include "stdafx.h"
#include <Windows.h>
#include <iostream>
#include <stdio.h>
#include "Class_SICK.h"

HANDLE hSerial;
DCB dcbSerialParams = { 0 };
COMMTIMEOUTS timeouts = { 0 };

Class_SICK::Class_SICK(){
}

Class_SICK::~Class_SICK(){
}

void Class_SICK::conectar(LPCWSTR port) {
	// Open the highest available serial port number
	fprintf(stderr, "Opening serial port...");
	hSerial = CreateFile(port, GENERIC_READ | GENERIC_WRITE, 0, NULL,	OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

	if (hSerial == INVALID_HANDLE_VALUE)
	{
		fprintf(stderr, "Error\n");
		return;
	}
	else fprintf(stderr, "OK\n");

	// Set device parameters (9600 baud, 1 start bit,
	// 1 stop bit, no parity)
	dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
	if (GetCommState(hSerial, &dcbSerialParams) == 0)
	{
		fprintf(stderr, "Error getting device state\n");
		CloseHandle(hSerial);
		return;
	}
	dcbSerialParams.BaudRate = CBR_9600;
	dcbSerialParams.DCBlength = 733;
	dcbSerialParams.ByteSize = 8;
	dcbSerialParams.StopBits = ONESTOPBIT;
	dcbSerialParams.Parity = NOPARITY;
	
}
