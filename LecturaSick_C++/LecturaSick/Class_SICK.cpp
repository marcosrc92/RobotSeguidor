#include "pch.h"
#include <Windows.h>
#include <iostream>
#include <stdio.h>
#include "Class_SICK.h"
#include <usb.h>
#include <fstream>

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
	hSerial = CreateFile(port, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);

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

	// Set device parameters (9600 baud, 1 start bit, 1 stop bit, no parity)
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
	dcbSerialParams.fDtrControl = FALSE;

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

int Class_SICK::reset() {
	//Datagrama de reset
	unsigned char msg_reset[] = { 0x02, 0x00, 0x01, 0x00, 0x10, 0x34, 0x12 };
	
	unsigned char respuesta_esperada[] = { 0x02, 0x80, 0x17, 0x00, 0x90, 0x4C, 0x4D, 0x53,
											0x32, 0x30, 0x30, 0x3B, 0x33, 0x30, 0x31, 0x30,
											0x36, 0x33, 0x3B, 0x56, 0x30, 0x32, 0x2E, 0x31,
											0x30, 0x20, 0x10, 0x63, 0x5E };

	//escribir en puerto USB
	DWORD bytes_written;
	DWORD bytes_read=0;
	BYTE response[30] = { 0x00 };

	fprintf(stderr, "Sending bytes...");
	//capturar error en la escritura
	if (!WriteFile(hSerial, msg_reset, 7, &bytes_written, NULL))
	{
		fprintf(stderr, "Error\n");
		CloseHandle(hSerial);
		return 1;
	}
	fprintf(stderr, "%d bytes written\n", bytes_written);
	
	fprintf(stderr, "Waiting response...");	
	//capturar el error en la lectura
	if (!ReadFile(hSerial, &response, 8, &bytes_read, NULL))
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
			return 1;
		}
	}
	
	while (*response != *respuesta_esperada) {
		ReadFile(hSerial, &response, 29, &bytes_read, NULL);
		Sleep(100);
		//datagrama de respuesta al reset
		for (int i = 0; i < bytes_read; i++) {
			//evita que entre la primera vez y escriba por pantalla
			if (i) {				
				//compruebo que la respuesta coincide con lo esperado
				if (response[i] != respuesta_esperada[i]) {
					cout << "Fallo de reset" << endl;
					return 1;
				}
				else printf("%02X ", response[i]);
			}
		}
	}

	cout << "\nbytes leidos: " << bytes_read << endl;
	fprintf(stderr, "Fin reset");
	return 0;
}

void Class_SICK::trama() {
	ofstream file;
	file.open("C:/Users/marco/OneDrive/Documentos/MAIIND/Robotica/RobotSeguidor/Map/Mapeado_consola/Mapeado(consola)/salidaDEC.txt");

	//Datagrama de grupo D
	unsigned char msg_medicion[] = { 0x02, 0x00, 0x02, 0x00, 0x30, 0x01, 0x31, 0x18 };

	//escribir en puerto USB
	DWORD bytes_written;
	DWORD bytes_read = 0;
	BYTE response[733] = { 0x00 };

	//while (1) {
		//Escrbir la trama de peticion de datos
		fprintf(stderr, "Sending bytes...");
		//capturar error en la escritura
		if (!WriteFile(hSerial, msg_medicion, 8, &bytes_written, NULL))
		{
			fprintf(stderr, "Error\n");
			CloseHandle(hSerial);
			return;
		}
		fprintf(stderr, "%d bytes written\n", bytes_written);

		//Leer buffer
		ReadFile(hSerial, &response, 733, &bytes_read, NULL);
		while (bytes_read < 733);

		//coordenadas polares recibidas en el buffer
		for (int i = 0; i < bytes_read; i++) {			
			printf("%d ", response[i]);
			//file << response[i] << endl;
		}
		cout << "\nbytes leidos: " << bytes_read << endl;
	//}
	return;
}