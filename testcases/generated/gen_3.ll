define i32 @factorial(i32 %n) {
entry:
  %result.addr = alloca i32, align 4
  store i32 1, i32* %result.addr, align 4
  br label %loop

loop:
  %i = phi i32 [ %n, %entry ], [ %i.next, %loop ]
  %result = load i32, i32* %result.addr, align 4
  %mul = mul nsw i32 %result, %i
  store i32 %mul, i32* %result.addr, align 4
  %i.next = add nsw i32 %i, -1
  %cond = icmp sgt i32 %i.next, 0
  br i1 %cond, label %loop, label %exit

exit:
  %result = load i32, i32* %result.addr, align 4
  ret i32 %result
}