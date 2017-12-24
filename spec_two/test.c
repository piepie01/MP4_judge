#include<stdio.h>
int main(){
	int a=0;
	for(long long i=0;i<200000000;i++){
		a+=i;
	}
	if(a==0) puts("hi");
	//printf("%d",a);
	return 0;
}
