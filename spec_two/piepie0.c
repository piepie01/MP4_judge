#include "../user_function.h"
int filter_function(struct User user) { int a=0; for(int i=0;i<10000000;i++){a++;} return (user.age == 0 );}