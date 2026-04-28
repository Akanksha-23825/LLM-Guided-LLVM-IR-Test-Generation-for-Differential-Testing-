define i32 @even(i32 %x) {
entry:
  %rem = urem i32 %x, 2
  %cond = icmp eq i32 %rem, 0
  %ret = select i1 %cond, i32 1, i32 0
  ret i32 %ret
}