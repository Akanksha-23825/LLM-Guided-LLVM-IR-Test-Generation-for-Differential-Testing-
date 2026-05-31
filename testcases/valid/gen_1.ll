define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp sgt i32 %a, %b
  br i1 %cmp, label %if.then, label %if.else
if.then:
  ret i32 %a
if.else:
  ret i32 %b
}