define i1 @greater_than_100(i32 %input) {
entry:
  %gt = icmp sgt i32 %input, 100
  ret i1 %gt
}