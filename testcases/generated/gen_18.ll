define i32 @loop_until_zero(i32 %value) {
entry:
  br i1 %cond, label %loop, label %exit

loop:
  %tmp = icmp eq i32 %value, 0
  br i1 %tmp, label %exit, label %loop

exit:
  ret i32 %value
  unreachable
}