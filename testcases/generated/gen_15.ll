define i32 @gcd(i32 %a, i32 %b) {
entry:
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %a, i32* %1, align 4
  store i32 %b, i32* %2, align 4
  br label %loop

loop:
  %4 = load i32, i32* %2, align 4
  %5 = icmp eq i32 %4, 0
  br i1 %5, label %out, label %loop_body

loop_body:
  %6 = load i32, i32* %1, align 4
  %7 = srem i32 %6, %4
  store i32 %7, i32* %1, align 4
  store i32 %4, i32* %2, align 4
  br label %loop

out:
  %8 = load i32, i32* %1, align 4
  ret i32 %8
}