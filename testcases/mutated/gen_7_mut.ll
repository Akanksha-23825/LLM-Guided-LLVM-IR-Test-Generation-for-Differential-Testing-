; Mutation: replaced constant 100 with 50
define i1 @greater_than_100(i32 %input) {
entry:
  %gt = icmp sgt i32 %input, 50
  ret i1 %gt
}