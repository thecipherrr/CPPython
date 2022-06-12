#include<iostream>
using namespace std;

void foo(auto a)
{
	cout << "hello world" << endl;
	cout << "baz" << endl;
}
int main(void)
{
	return 0;
}