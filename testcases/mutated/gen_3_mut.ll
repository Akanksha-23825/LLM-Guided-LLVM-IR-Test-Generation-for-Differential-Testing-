; Mutation: added dead computation with result %14
define i32 @factorial(i32 %n) {
entry:
  %1 = alloca i32
  store i32 %n, i32* %1
  %2 = load i32, i32* %1
  %3 = icmp eq i32 %2, 0
  br i1 %3, label %if.then, label %if.else

if.then:
  %4 = mul i32 1, 1
  br label %if.end

if.else:
  %5 = load i32, i32* %1
  %6 = mul i32 %5, 1
  %7 = sub i32 %5, 1
  store i32 %7, i32* %1
  br label %if.cont

if.cont:
  %8 = load i32, i32* %1
  %9 = call i32 @factorial(i32 %8)
  %10 = mul i32 %6, %9
  %11 = load i32, i32* %1
  br label %if.end

if.end:
  %12 = load i32, i32* %1
  %13 = mul i32 1, %12
  %14 = add i32 %12, %12
  ret i32 %13
}