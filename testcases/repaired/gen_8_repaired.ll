define i32 @sum_loop(i32 %n) {
entry:
  %1 = add i32 1, 0
  %2 = phi i32 [ %1, %entry ], [ %6, %loop ]
  %3 = icmp slt i32 %2, %n
  br i1 %3, label %loop, label %exit
loop:
  %4 = add i32 %2, 1
  %5 = mul i32 %2, %4
  %6 = add i32 %5, %2
  br label %loop
exit:
  ret i32 %6
}