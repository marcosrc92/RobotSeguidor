#pragma once
#include <Windows.h>
#include "pch.h"

class Class_SICK
{
public:
	Class_SICK();
	~Class_SICK();
	
	void conectar(LPCWSTR);
	void reset();
};

