define i32 @loop_until_zero(i32 %1) {
entry:
  %2 = icmp eq i32 %1, 0
  br i1 %2, label %exit, label %loop

loop:
  %3 = icmp eq i32 %1, 0
  br i1 %3, label %exit, label %loop

exit:
  ret i32 %1
}