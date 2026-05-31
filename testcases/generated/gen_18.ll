define i32 @loop_until_zero(i32 %value) {
entry:
  %tmp = icmp slt i32 %value, 0
  br i1 %tmp, label %exit, label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %i.next = add nsw i32 %i, 1
  %tmp2 = icmp slt i32 %i.next, %value
  br i1 %tmp2, label %loop, label %exit

exit:
  ret i32 %i
}