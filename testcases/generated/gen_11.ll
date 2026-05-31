define i32 @loop(i32 %n) {
entry:
  %i = phi i32 [0, %entry], [%i.next, %loop]
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit
exit:
  %0 = phi i32 [%n, %loop], [%i.next, %exit]
  ret i32 %0
}