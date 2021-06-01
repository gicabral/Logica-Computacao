int soma(int x, int y) {
int a;
int d;
a = x + y;
println(a);
return a;
}
int main() {
int a;
int b;
a = 3;
while (a < 6){
    b = soma(a, 4);
    a = a + 1;
}
println(a);
println(b);
}
