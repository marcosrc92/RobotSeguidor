#include "stdafx.h"
#include "Class_SICK.h"
#include "Mapeado.h"
#include <iostream>
#include <stdio.h>

using namespace std;

int main() {
	
	Class_SICK sick;
	LPCWSTR puerto = TEXT("\\.\COM1");
	
	sick.conectar(puerto);

	system("PAUSE");
	return 0;
}