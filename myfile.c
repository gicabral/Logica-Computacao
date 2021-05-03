{
i = 1;
n = 15;
y = 4;
x = 1;
while (i < n || i == n) {
if (x > y)
y = y + 1;
else if (x < y)
x = x + 1;
else {
x = x + i;
println(x);
println(y);
}
i = i + 1;
}
println(readln());
;
;
;
;
}