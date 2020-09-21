#include "bip39.c"
#include <stdio.h>

int main(){
	const char *in ="garden reject beauty inch scissors rifle amazing couch bacon multiply swim poverty impose spray ugly term stamp prevent nothing mutual awful project wrist movie";
	uint8_t entropy;
	printf("Func returned: %d\n",mnemonic_to_entropy(in,&entropy));
	printf("entropy is: %d",entropy);
	return 0;
}
