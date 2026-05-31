define i64 @power(i64 %x, i64 %n) {
entry:
  %0 = icmp eq i64 %n, 0
  br i1 %0, label %if.then, label %if.else

if.then:
  ret i64 1

if.else:
  %2 = icmp ugt i64 %n, 1
  %3 = select i1 %2, i64 %n, i64 1
  %4 = mul i64 %x, %x
  %5 = icmp eq i64 %3, 1
  br i1 %5, label %if.then1, label %if.else1

if.then1:
  ret i64 %4

if.else1:
  %7 = sub i64 %3, 1
  %8 = mul i64 %4, %x
  %9 = call i64 @power(i64 %x, i64 %7)
  %10 = mul i64 %8, %9
  ret i64 %10
}