define i32 @even(i32 %x) {
entry:
  %rem = urem i32 %x, 2
  %cond = icmp eq i32 %rem, 0
  br i1 %cond, label %even, label %odd
even:
  ret i32 1
odd:
  ret i32 0
}