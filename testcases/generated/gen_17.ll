define i32 @chain_compare(i32 %a, i32 %b, i32 %c, i32 %d, i32 %e, i32 %f, i32 %g, i32 %h) {
entry:
  %0 = icmp sgt i32 %a, 0
  br i1 %0, label %then0, label %else0

then0:
  %1 = icmp sgt i32 %b, %a
  br i1 %1, label %then1, label %else1

then1:
  %2 = icmp sgt i32 %c, %b
  br i1 %2, label %then2, label %else2

then2:
  %3 = icmp sgt i32 %d, %c
  br i1 %3, label %then3, label %else3

then3:
  %4 = icmp sgt i32 %e, %d
  br i1 %4, label %then4, label %else4

then4:
  %5 = icmp sgt i32 %f, %e
  br i1 %5, label %then5, label %else5

then5:
  %6 = icmp sgt i32 %g, %f
  br i1 %6, label %then6, label %else6

then6:
  %7 = icmp sgt i32 %h, %g
  br i1 %7, label %then7, label %else7

then7:
  ret i32 %h
else7:
  unreachable

else6:
  %8 = icmp sgt i32 %g, %f
  br i1 %8, label %then8, label %else8

then8:
  ret i32 %g
else8:
  unreachable

else5:
  %9 = icmp sgt i32 %f, %e
  br i1 %9, label %then9, label %else9

then9:
  ret i32 %f
else9:
  unreachable

else4:
  %10 = icmp sgt i32 %e, %d
  br i1 %10, label %then10, label %else10

then10:
  ret i32 %e
else10:
  unreachable

else3:
  %11 = icmp sgt i32 %d, %c
  br i1 %11, label %then11, label %else11

then11:
  ret i32 %d
else11:
  unreachable

else2:
  %12 = icmp sgt i32 %c, %b
  br i1 %12, label %then12, label %else12

then12:
  ret i32 %c
else12:
  unreachable

else1:
  %13 = icmp sgt i32 %b, %a
  br i1 %13, label %then13, label %else13

then13:
  ret i32 %b
else13:
  unreachable

else0:
  ret i32 %a
}