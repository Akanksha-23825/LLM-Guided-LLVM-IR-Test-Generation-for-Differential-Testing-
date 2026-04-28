; Mutation: added dead computation for unused result of i32 addition
define i32 @factorial(i32 %n) {
entry:
  %1 = alloca i32
  store i32 1, i32* %1
  br label %loop

loop:
  %2 = load i32, i32* %1
  %3 = icmp sgt i32 %n, 1
  br i1 %3, label %loop_body, label %exit

loop_body:
  %4 = load i32, i32* %1
  %5 = mul nsw i32 %4, %n
  store i32 %5, i32* %1
  %6 = load i32, i32* %1
  %7 = sub i32 %n, 1
  store i32 %7, i32* %1
  %9 = add nsw i32 %7, 2
  br label %loop

exit:
  %8 = load i32, i32* %1
  ret i32 %8
}