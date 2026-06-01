define i32 @gcd(i32 %0, i32 %1) {
entry:
  %2 = icmp sgt i32 %0, 0
  %3 = icmp sgt i32 %1, 0
  %4 = and i1 %2, %3
  br i1 %4, label %5, label %6

5:
  %7 = srem i32 %1, %0
  %8 = icmp eq i32 %7, 0
  br i1 %8, label %6, label %5

6:
  %9 = icmp eq i32 %0, %1
  br i1 %9, label %10, label %11

10:
  %12 = phi i32 [ %0, %5 ], [ %1, %6 ]
  %13 = phi i32 [ %0, %5 ], [ %1, %6 ]
  ret i32 %12

11:
  %14 = add i32 %0, %1
  %15 = sdiv i32 %14, 2
  %16 = srem i32 %0, %15
  %17 = icmp eq i32 %16, 0
  br i1 %17, label %18, label %19

18:
  %20 = phi i32 [ %14, %11 ], [ %1, %6 ]
  ret i32 %20

19:
  %21 = phi i32 [ %14, %11 ], [ %0, %6 ]
  %22 = phi i32 [ %14, %11 ], [ %1, %6 ]
  br label %5

unreachable
}