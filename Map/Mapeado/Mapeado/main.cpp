#include "stdafx.h"
#include "Class_SICK.h"
#include "Mapeado.h"
#include <iostream>


int main() {
	
	Class_SICK sick;
	LPCWSTR puerto = TEXT("\\.\COM1");

	sick.conectar(puerto);

	system("PAUSE");
	return 0;
}