#define USER_NAME_LEN 33
#define INTRO_LEN 1025
struct User{
	char name[USER_NAME_LEN];
	unsigned int age;
	char gender[7];
	char introduction[INTRO_LEN];
};
