define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp slt i32 %a, %b
  br i1 %cmp, label %if.then, label %if.else

if.then:
  %0 = phi i32 [ %b, %entry ], [ %a, %if.else ]
  ret i32 %0

if.else:
  %1 = phi i32 [ %b, %entry ], [ %a, %if.then ]
  ret i32 %1
}