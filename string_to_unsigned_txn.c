#include<stdio.h>
#include"BTC_btc.h"

unsigned_txn* string_to_unsigned_txn(const char* received){
	const char* temp=received;
	
	unsigned_txn* result=(unsigned_txn*)malloc(sizeof(unsigned_txn));

	int conv;
	for(int i=0;i<4;i++){
		sscanf(temp,"%x",&conv);
		result->network_version[i]=conv;
		temp+=2;
	}
	sscanf(temp,"%x",&conv);
	result->input_count[0]=conv;
	temp+=2;

	result->input=(unsigned_txn_input*)malloc(sizeof(unsigned_txn_input)*(*result->input_count));
	for(size_t count=0;count<conv;count++){
		unsigned_txn_input transition;
		for(size_t l=0;l<32;l++){
			sscanf(temp,"%x",&conv);
			temp+=2;
			transition.previous_txn_hash[l]=conv;
		}

		for(size_t l=0;l<4;l++){
			sscanf(temp,"%x",&conv);
			temp+=2;
			transition.previous_output_index[l]=conv;
		}
		sscanf(temp,"%x",&conv);
		transition.script_length[0]=conv;
		temp+=2;	
		for(size_t l=0;l<25;l++){
                        sscanf(temp,"%x",&conv);
                        temp+=2;
                        transition.script_public_key[l]=conv;
                }

		for(size_t l=0;l<4;l++){
                        sscanf(temp,"%x",&conv);
                        temp+=2;
                        transition.sequence[l]=conv;
		}

		result->input[count]=transition;
		
	}

	sscanf(temp,"%x",&conv);
	result->output_count[0]=conv;
        temp+=2;
	result->output=(txn_output*)malloc(sizeof(txn_output)*(*result->output_count));
       
	for(size_t count=0;count<conv;count++){
		txn_output transition;
		for(size_t l=0;l<8;l++){
			sscanf(temp,"%x",&conv);
			temp+=2;
			transition.value[l]=conv;
		}

		sscanf(temp,"%x",&conv);
		transition.script_length[0]=conv;
		temp+=2;
		for(size_t l=0;l<25;l++){
			sscanf(temp,"%x",&conv);
			temp+=2;
			transition.script_public_key[l]=conv;
		}
		result->output[count]=transition;
	}
	for(int i=0;i<4;i++){
                sscanf(temp,"%x",&conv);
		result->locktime[i]=conv;
                temp+=2;
        }


	for(int i=0;i<4;i++){
                sscanf(temp,"%x",&conv);
		result->sighash[i]=conv;
                temp+=2;
        }
	return result;
}

int main(){
	const char *received_unsigned_txn_string ="0200000001748dccb662fd73e8f0d8435132b8528dd3739f55388a15795c7e7afe4f555f9f010000001976a9140ce400ffe51ab038f6134beeb14ef56c683ce00088acfdffffff02204e0000000000001976a914d46d05e6ac27683aa5d63a6efc44969798acf13688ac28b30000000000001976a914dacc24d8b195ce046a40caedd5e2e649beee4e3388ac49211a0001000000";
	printf("%s\n",received_unsigned_txn_string);
	string_to_unsigned_txn(received_unsigned_txn_string);
	return 0;
}
