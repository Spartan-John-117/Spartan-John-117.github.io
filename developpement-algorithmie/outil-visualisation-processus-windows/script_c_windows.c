#include <windows.h>
#include <tlhelp32.h>
#include <tchar.h>
#include <stdio.h>

BOOL GetProcessList();
void printError(TCHAR const* msg);
void PrintElapsedTime(SYSTEMTIME startTime);

int main(void)
{
    GetProcessList();
    return 0;
}

BOOL GetProcessList()
{
    HANDLE hProcessSnap;
    HANDLE hProcess;
    PROCESSENTRY32 pe32;
    FILETIME creationTime, exitTime, kernelTime, userTime;
    SYSTEMTIME systemStartTime;
    DWORD dwPriorityClass;

    // Take a snapshot of all processes in the system.
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE)
    {
        printError(TEXT("CreateToolhelp32Snapshot (of processes)"));
        return (FALSE);
    }

    // Set the size of the structure before using it.
    pe32.dwSize = sizeof(PROCESSENTRY32);

    // Retrieve information about the first process, and exit if unsuccessful
    if (!Process32First(hProcessSnap, &pe32))
    {
        printError(TEXT("Process32First"));
        CloseHandle(hProcessSnap);
        return (FALSE);
    }

    // Print the header
    _tprintf(TEXT("%-40s %-10s %-8s %-10s %-10s %-10s %-15s %-15s\n"),
        TEXT("Name"), TEXT("Pid"), TEXT("Pri"), TEXT("Thd"),
        TEXT("Hnd"), TEXT("Priv"), TEXT("CPU Time"), TEXT("Elapsed Time"));

    // Walk the snapshot of processes
    do
    {
        hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pe32.th32ProcessID);

        dwPriorityClass = 0;
		if (hProcess == NULL)
        {
            _tprintf(TEXT("%-40s %-10d %-8s %-10d %-10d %-10s %-15s %-15s\n"),
                pe32.szExeFile, pe32.th32ProcessID, TEXT("-"), pe32.cntThreads,
                pe32.cntUsage, TEXT("-"), TEXT("-"), TEXT("-"));
			continue;
        }
        dwPriorityClass = GetPriorityClass(hProcess);

        // Retrieve CPU and elapsed time
        if (!GetProcessTimes(hProcess, &creationTime, &exitTime, &kernelTime, &userTime))
        {
            continue;
        }
        SYSTEMTIME userSystemTime;
        FileTimeToSystemTime(&userTime, &userSystemTime);
        FileTimeToSystemTime(&creationTime, &systemStartTime);

        _tprintf(TEXT("%-40s %-10d %-8d %-10d %-10d %-10lu %02d:%02d:%02d.%03d  "),
            pe32.szExeFile,
            pe32.th32ProcessID,
            dwPriorityClass,
            pe32.cntThreads,
            pe32.cntUsage, // Handle count not available directly; using cntUsage as an approximation
            pe32.dwSize / 1024, // Approximation of private memory usage
            userSystemTime.wHour, userSystemTime.wMinute, userSystemTime.wSecond, userSystemTime.wMilliseconds);

        // Print elapsed time
        PrintElapsedTime(systemStartTime);

        CloseHandle(hProcess);

        
    } while (Process32Next(hProcessSnap, &pe32));

    CloseHandle(hProcessSnap);
    return (TRUE);
}

void PrintElapsedTime(SYSTEMTIME startTime)
{
    SYSTEMTIME currentTime;
    GetSystemTime(&currentTime);

    FILETIME ftStart, ftCurrent;
    ULARGE_INTEGER ulStart, ulCurrent;

    SystemTimeToFileTime(&startTime, &ftStart);
    SystemTimeToFileTime(&currentTime, &ftCurrent);

    ulStart.LowPart = ftStart.dwLowDateTime;
    ulStart.HighPart = ftStart.dwHighDateTime;
    ulCurrent.LowPart = ftCurrent.dwLowDateTime;
    ulCurrent.HighPart = ftCurrent.dwHighDateTime;

    ULONGLONG elapsed = (ulCurrent.QuadPart - ulStart.QuadPart) / 10000000ULL; // Convert from 100-nanosecond intervals to seconds

    int days = elapsed / (24 * 3600);
    elapsed %= (24 * 3600);
    int hours = elapsed / 3600;
    elapsed %= 3600;
    int minutes = elapsed / 60;
    int seconds = elapsed % 60;

    if (days > 0)
        _tprintf(TEXT("%dd %02d:%02d:%02d\n"), days, hours, minutes, seconds);
    else
        _tprintf(TEXT("%02d:%02d:%02d\n"), hours, minutes, seconds);
}

void printError(TCHAR const* msg)
{
    DWORD eNum;
    TCHAR sysMsg[256];
    TCHAR* p;

    eNum = GetLastError();
    FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL, eNum,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        sysMsg, 256, NULL);

    p = sysMsg;
    while ((*p > 31) || (*p == 9))
        ++p;
    do
    {
        *p-- = 0;
    } while ((p >= sysMsg) && ((*p == '.') || (*p < 33)));

    _tprintf(TEXT("\n  WARNING: %s failed with error %d (%s)"), msg, eNum, sysMsg);
}

