; Mutation: renamed SSA variable %0 to %is_positive
define i32 @abs(i32 %x) {
entry:
  %is_positive = icmp sgt i32 %x, 0
  %1 = select i1 %is_positive, i32 %x, i32 %x
  ret i32 %1
}