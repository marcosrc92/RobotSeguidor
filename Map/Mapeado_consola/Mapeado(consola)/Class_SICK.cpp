#include "pch.h"
#include <Windows.h>
#include <iostream>
#include <stdio.h>
#include "Class_SICK.h"
#include <usb.h>

using namespace std;

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
	hSerial = CreateFile(port, GENERIC_READ | GENERIC_WRITE, 0, NULL,	OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);

	//capturar el error
	if (hSerial == INVALID_HANDLE_VALUE)
	{
		fprintf(stderr, "Error\n");
				
		DWORD errorMessageID = ::GetLastError();
		LPSTR messageBuffer = nullptr;

		size_t size = FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
			NULL, errorMessageID, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR)&messageBuffer, 0, NULL);

		//Liberar el buffer.
		LocalFree(messageBuffer);

		//https://docs.microsoft.com/en-us/windows/desktop/debug/system-error-codes--0-499-
		printf("La ID de error es: %d\n", errorMessageID);
		switch (errorMessageID)
		{
		case 2:
			printf("The system cannot find the file specified\n");
			break;
		default:
			break;
		}
		CloseHandle(hSerial);
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
	dcbSerialParams.BaudRate = 9600;
	dcbSerialParams.DCBlength = 733;
	dcbSerialParams.ByteSize = 8;
	dcbSerialParams.StopBits = ONESTOPBIT;
	dcbSerialParams.Parity = NOPARITY;

	SetCommState(hSerial, &dcbSerialParams);

	// Set COM port timeout settings
	timeouts.ReadIntervalTimeout = 500;
	timeouts.ReadTotalTimeoutConstant = 50;
	timeouts.ReadTotalTimeoutMultiplier = 10;
	timeouts.WriteTotalTimeoutConstant = 50;
	timeouts.WriteTotalTimeoutMultiplier = 10;
	if (SetCommTimeouts(hSerial, &timeouts) == 0)
	{
		fprintf(stderr, "Error setting timeouts\n");
		CloseHandle(hSerial);
		return;
	}
	
}

void Class_SICK::reset() {
	//Datagrama de reset
	unsigned char msg_reset[] = { 0x02, 0x00, 0x01, 0x00, 0x10, 0x34, 0x12 };
	//char msg_reset_int[] = {2, 0, 1, 0, 16, 52, 18};

	//escribir en puerto USB
	DWORD bytes_written;
	LPDWORD bytes_read=0;
	LPVOID response;

	fprintf(stderr, "Sending bytes...");
	//capturar error en la escritura
	if (!	WriteFile(hSerial, msg_reset, 7, &bytes_written, NULL))
	{
		fprintf(stderr, "Error\n");
		CloseHandle(hSerial);
		return;
	}
	fprintf(stderr, "%d bytes written\n", bytes_written);
	
	fprintf(stderr, "Waiting response...");	
	//capturar el error en la lectura
	if (!ReadFile(hSerial, &response, 8, bytes_read, NULL))
	{
		fprintf(stderr, "Error\n");


		DWORD errorMessageID = ::GetLastError();
		LPSTR messageBuffer = nullptr;

		size_t size = FormatMessageA(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
			NULL, errorMessageID, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR)&messageBuffer, 0, NULL);

		//Liberar el buffer.
		LocalFree(messageBuffer);

		//https://docs.microsoft.com/en-us/windows/desktop/debug/system-error-codes--0-499-
		printf("La ID de error es: %d\n", errorMessageID);
		switch (errorMessageID)
		{
		case 998:
			printf("Invalid access to memory location\n");
			break;
		default:
			break;

			CloseHandle(hSerial);
			return;
		}
	}

	//datagrama de respuesta al reset
	cout << response << endl;
}