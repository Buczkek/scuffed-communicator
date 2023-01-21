// C++ program to find factorial of given number
#include <iostream>
using namespace std;

// function to find factorial of given number
unsigned long long factorial(unsigned long n)
{
    if (n == 0)
        return 1;
    return n * factorial(n - 1);
}

// Driver code
int main()
{
    long num;
    cin >> num;
    cout << factorial(num) << endl;
    return 0;
}