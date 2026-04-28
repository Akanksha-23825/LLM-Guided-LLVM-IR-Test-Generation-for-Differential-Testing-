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
should be rewritten as 
define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp slt i32 %a, %b
  br i1 %cmp, label %if.then, label %if.else

if.then:
  %0 = phi i32 [ %b, %entry ]
  ret i32 %0

if.else:
  %1 = phi i32 [ %b, %entry ]
  ret i32 %1
} 
However, this is still not correct as there is no %a in the phi node of if.then and if.else. 
The correct phi node should be 
if.then:
  %0 = phi i32 [ %b, %entry ]
if.else:
  %1 = phi i32 [ %a, %entry ]
However, this will not work as there is no way to get the value of %a in if.then and %b in if.else.
The correct code should be 
define i32 @max(i32 %a, i32 %b) {
entry:
  %cmp = icmp slt i32 %a, %b
  br i1 %cmp, label %if.then, label %if.else

if.then:
  ret i32 %b

if.else:
  ret i32 %a
}