define i32 @gcd(i32 %x, i32 %y) {
entry:
  %1 = icmp sgt i32 %x, 0
  %2 = icmp sgt i32 %y, 0
  %cond = and i1 %1, %2
  br i1 %cond, label %loop, label %if.end

loop:
  %3 = srem i32 %y, %x
  %4 = icmp eq i32 %3, 0
  br i1 %4, label %if.end, label %loop

if.end:
  %5 = icmp eq i32 %x, %y
  br i1 %5, label %if.then, label %if.else

if.then:
  %6 = phi i32 [ %x, %loop ], [ %y, %if.end ]
  %7 = phi i32 [ %x, %loop ], [ %y, %if.end ]
  ret i32 %6

if.else:
  %8 = add i32 %x, %y
  %9 = sdiv i32 %8, 2
  %10 = srem i32 %x, %9
  %11 = icmp eq i32 %10, 0
  br i1 %11, label %if.then2, label %if.else2

if.then2:
  %12 = phi i32 [ %8, %if.else ], [ %y, %if.end ]
  ret i32 %12

if.else2:
  %13 = phi i32 [ %8, %if.else ], [ %x, %if.end ]
  %14 = phi i32 [ %8, %if.else ], [ %y, %if.end ]
  br label %loop, %phi_args = { i32 %13, i32 %14 }

unreachable
}