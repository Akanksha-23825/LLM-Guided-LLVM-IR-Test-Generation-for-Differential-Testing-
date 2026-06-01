define i32 @fizzbuzz(i32 %1, i32 %2) {
entry:
  %3 = icmp eq i32 %2, 0
  br i1 %3, label %4, label %5

inc:
  %6 = add i32 %2, 1
  %7 = icmp eq i32 %6, 0
  br i1 %7, label %4, label %8

loop:
  %9 = phi i32 [ %6, %5 ], [ 0, %entry ]
  %10 = icmp eq i32 %9, 15
  %11 = icmp eq i32 %9, 3
  %12 = select i1 %10, i32 0, i32 (select i1 %11, i32 0, i32 %9)
  %13 = add i32 %12, %9
  store i32 %13, i32* @result_array, align 4
  %14 = add i32 %9, 1
  %15 = icmp eq i32 %14, %1
  br i1 %15, label %4, label %5

end:
  ret i32 0
}