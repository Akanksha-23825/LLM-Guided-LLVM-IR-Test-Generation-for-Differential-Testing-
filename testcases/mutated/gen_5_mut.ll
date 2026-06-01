; Mutation: renamed SSA variable %mul to %product
define i32 @multiply(i32 %a, i32 %b) {
entry:
  %product = mul i32 %a, %b
  ret i32 %product
}