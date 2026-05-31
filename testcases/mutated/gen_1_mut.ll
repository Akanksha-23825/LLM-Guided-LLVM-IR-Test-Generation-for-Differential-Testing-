; Mutation: no arithmetic operator to swap, adding a new one and then swapping it
define i32 @max(i32 %a, i32 %b) {
entry:
  %add = add i32 %a, %b
  %mul = mul i32 %add, 1
  %cmp = icmp sgt i32 %a, %b
  br i1 %cmp, label %if.then, label %if.else
if.then:
  ret i32 %a
if.else:
  ret i32 %b
}