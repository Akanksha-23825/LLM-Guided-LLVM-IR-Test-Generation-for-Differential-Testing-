define i32 @abs(i32 %x) {
entry:
  %ge = icmp sgt i32 %x, 0
  %lt = icmp slt i32 %x, 0
  %select = select i1 %ge, i32 %x, i32 -%x
  ret i32 %select
}