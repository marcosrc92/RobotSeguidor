// Mapeado(consola).cpp : Este archivo contiene la función "main". La ejecución del programa comienza y termina ahí.

#include "pch.h"
#include <iostream>
#include "Class_SICK.h"

int main()
{
	Class_SICK sick;
	LPCWSTR puerto=TEXT("COM1");

	sick.conectar(puerto);
	
	sick.reset();

	//sick.trama();
}