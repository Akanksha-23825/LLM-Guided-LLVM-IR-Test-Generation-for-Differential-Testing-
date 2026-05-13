; Mutation: renamed SSA variable %cmp to %comparison
define i32 @max(i32 %a, i32 %b) {
entry:
  %comparison = icmp sgt i32 %a, %b
  br i1 %comparison, label %then, label %else

then:
  ret i32 %a

else:
  ret i32 %b
}