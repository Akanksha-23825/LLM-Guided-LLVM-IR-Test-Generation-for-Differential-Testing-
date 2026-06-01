define i32 @add(i32, i32) {
entry:
  %1 = alloca i32
  %2 = alloca i32
  store i32 %0, i32* %1
  store i32 %1, i32* %2
  %3 = load i32, i32* %1
  %4 = load i32, i32* %2
  %sum = add nsw i32 %3, %4
  ret i32 %sum
}