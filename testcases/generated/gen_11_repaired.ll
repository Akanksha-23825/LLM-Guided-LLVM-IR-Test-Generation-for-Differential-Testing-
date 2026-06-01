define i32 @count_to_twenty() {
entry:
  %1 = alloca i32
  store i32 0, i32* %1
  br label %2

2:
  %3 = load i32, i32* %1
  %4 = icmp slt i32 %3, 21
  %5 = add i32 %3, 1
  %6 = phi i32 [ %3, %entry ], [ %5, %2 ]
  %7 = phi i32 [ 0, %entry ], [ %5, %2 ]
  store i32 %6, i32* %1
  %8 = icmp eq i32 %7, 20
  br i1 %4, label %2, label %9

9:
  ret i32 %7
}