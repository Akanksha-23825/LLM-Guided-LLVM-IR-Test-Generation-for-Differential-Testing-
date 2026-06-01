; Mutation: added dead computation with result never used
define i32 @factorial(i32 %n) {
entry:
  %n.addr = alloca i32, align 4
  store i32 %n, i32* %n.addr, align 4
  br label %loop

loop:
  %0 = load i32, i32* %n.addr, align 4
  %1 = sub i32 %0, 1
  store i32 %1, i32* %n.addr, align 4
  %2 = load i32, i32* %n.addr, align 4
  %3 = load i32, i32* %n.addr, align 4
  %mul = mul nsw i32 %2, %3
  store i32 %mul, i32* %n.addr, align 4
  %4 = load i32, i32* %n.addr, align 4
  %5 = icmp slt i32 %4, 1
  %dead = add i32 %4, 10
  br i1 %5, label %if.then, label %loop

if.then:
  %6 = load i32, i32* %n.addr, align 4
  ret i32 %6
}