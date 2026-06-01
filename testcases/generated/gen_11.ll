define i32 @count_to_twenty() {
entry:
  %i = alloca i32
  store i32 0, i32* %i
  br label %loop

loop:
  %i_val = load i32, i32* %i
  %cond = icmp slt i32 %i_val, 21
  %i_next = add i32 %i_val, 1
  %phi_val = phi i32 [ %i_val, %entry ], [ %i_next, %loop ]
  store i32 %phi_val, i32* %i
  %i_loop = phi i32 [ 0, %entry ], [ %i_next, %loop ]
  %end = icmp eq i32 %i_loop, 20
  br i1 %cond, label %loop, label %end_label

end_label:
  ret i32 %i_loop
}