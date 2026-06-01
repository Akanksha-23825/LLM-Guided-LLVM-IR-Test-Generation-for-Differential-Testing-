define i32 @max(i32 %a, i32 %b) {
entry:
  %compare = icmp ult i32 %a, %b
  br i1 %compare, label %if.then, label %if.else

if.then:
  %max1 = phi i32 [ %b, %entry ], [ %b, %if.else ]
  ret i32 %max1

if.else:
  %max2 = phi i32 [ %a, %entry ], [ %a, %if.then ]
  ret i32 %max2
}