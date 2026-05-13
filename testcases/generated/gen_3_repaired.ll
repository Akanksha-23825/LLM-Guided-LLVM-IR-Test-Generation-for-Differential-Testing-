define i32 @factorial(i32 %0) {
entry:
  %1 = alloca i32, align 4
  store i32 1, i32* %1, align 4
  br label %loop

loop:
  %2 = phi i32 [ %0, %entry ], [ %3, %loop ]
  %4 = load i32, i32* %1, align 4
  %5 = mul nsw i32 %4, %2
  store i32 %5, i32* %1, align 4
  %3 = add nsw i32 %2, -1
  %6 = icmp sgt i32 %3, 0
  br i1 %6, label %loop, label %exit

exit:
  %7 = load i32, i32* %1, align 4
  ret i32 %7
}