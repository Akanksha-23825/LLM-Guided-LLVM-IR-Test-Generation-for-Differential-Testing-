define i32 @fizzbuzz(i32 %i) {
entry:
  %1 = icmp sgt i32 %i, 0
  br i1 %1, label %if.then, label %if.else

if.then:
  %2 = srem i32 %i, 3
  %3 = srem i32 %i, 5
  %4 = icmp eq i32 %2, 0
  %5 = icmp eq i32 %3, 0
  %6 = or i1 %4, %5
  br i1 %6, label %if.then2, label %if.else2

if.then2:
  %7 = mul nsw i32 %i, 3
  %8 = add nsw i32 %i, 1
  %9 = mul nsw i32 %8, 5
  %10 = mul nsw i32 %7, 1
  %11 = sub nsw i32 %9, %10
  %12 = zext i32 %11 to i64
  %13 = zext i32 %i to i64
  %14 = icmp slt i64 %13, 16
  br i1 %14, label %if.then3, label %if.else3

if.then3:
  %15 = mul nsw i64 %12, 1
  %16 = sdiv i64 %15, 1
  %17 = trunc i64 %16 to i32
  ret i32 %17

if.else2:
  %18 = srem i32 %i, 3
  %19 = srem i32 %i, 5
  %20 = icmp eq i32 %18, 0
  %21 = icmp eq i32 %19, 0
  %22 = or i1 %20, %21
  br i1 %22, label %if.then4, label %if.else4

if.then4:
  %23 = mul nsw i32 %i, 3
  %24 = add nsw i32 %i, 1
  %25 = mul nsw i32 %24, 5
  %26 = mul nsw i32 %23, 1
  %27 = sub nsw i32 %25, %26
  %28 = zext i32 %27 to i64
  %29 = zext i32 %i to i64
  %30 = icmp slt i64 %29, 16
  br i1 %30, label %if.then5, label %if.else5

if.then5:
  %31 = mul nsw i64 %28, 1
  %32 = sdiv i64 %31, 1
  %33 = trunc i64 %32 to i32
  ret i32 %33

if.else4:
  %34 = srem i32 %i, 3
  %35 = srem i32 %i, 5
  %36 = icmp eq i32 %34, 0
  %37 = icmp eq i32 %35, 0
  %38 = or i1 %36, %37
  br i1 %38, label %if.then6, label %if.else6

if.then6:
  %39 = mul nsw i32 %i, 3
  %40 = add nsw i32 %i, 1
  %41 = mul nsw i32 %40, 5
  %42 = mul nsw i32 %39, 1
  %43 = sub nsw i32 %41, %42
  %44 = zext i32 %43 to i64
  %45 = zext i32 %i to i64
  %46 = icmp slt i64 %45, 16
  br i1 %46, label %if.then7, label %if.else7

if.then7:
  %47 = mul nsw i64 %44, 1
  %48 = sdiv i64 %47, 1
  %49 = trunc i64 %48 to i32
  ret i32 %49

if.else5:
  %50 = srem i32 %i, 3
  %51 = srem i32 %i, 5
  %52 = icmp eq i32 %50, 0
  %53 = icmp eq i32 %51, 0
  %54 = or i1 %52, %53
  br i1 %54, label %if.then8, label %if.else8

if.then8:
  %55 = mul nsw i32 %i, 3
  %56 = add nsw i32 %i, 1
  %57 = mul nsw i32 %56, 5
  %58 = mul nsw i32 %55, 1
  %59 = sub nsw i32 %57, %58
  %60 = zext i32 %59 to i64
  %61 = zext i32 %i to i64
  %62 = icmp slt i64 %61, 16
  br i1 %62, label %if.then9, label %if.else9

if.then9:
  %63 = mul nsw i64 %60, 1
  %64 = sdiv i64 %63, 1
  %65 = trunc i64 %64 to i32
  ret i32 %65

if.else6:
  %66 = srem i32 %i, 3
  %67 = srem i32 %i, 5
  %68 = icmp eq i32 %66, 0
  %69 = icmp eq i32 %67, 0
  %70 = or i1 %68, %69
  br i1 %70, label %if.then10, label %if.else10

if.then10:
  %71 = mul nsw i32 %i, 3
  %72 = add nsw i32 %i, 1
  %73 = mul nsw i32 %72, 5
  %74 = mul nsw i32 %71, 1
  %75 = sub nsw i32 %73, %74
  %76 = zext i32 %75 to i64
  %77 = zext i32 %i to i64
  %78 = icmp slt i64 %77, 16
  br i1 %78, label %if.then11, label %if.else11

if.then11:
  %79 = mul nsw i64 %76, 1
  %80 = sdiv i64 %79, 1
  %81 = trunc i64 %80 to i32
  ret i32 %81

if.else7:
  %82 = srem i32 %i, 3
  %83 = srem i32 %i, 5
  %84 = icmp eq i32 %82, 0
  %85 = icmp eq i32 %83, 0
  %86 = or i1 %84, %85
  br i1 %86, label %if.then12, label %if.else12

if.then12:
  %87 = mul nsw i32 %i, 3
  %88 = add nsw i32 %i, 1
  %89 = mul nsw i32 %88, 5
  %90 = mul nsw i32 %87, 1
  %91 = sub nsw i32 %89, %90
  %92 = zext i32 %91 to i64
  %93 = zext i32 %i to i64
  %94 = icmp slt i64 %93, 16
  br i1 %94, label %if.then13, label %if.else13

if.then13:
  %95 = mul nsw i64 %92, 1
  %96 = sdiv i64 %95, 1
  %97 = trunc i64 %96 to i32
  ret i32 %97

if.else8:
  %98 = srem i32 %i, 3
  %99 = srem i32 %i, 5
  %100 = icmp eq i32 %98, 0
  %101 = icmp eq i32 %99, 0
  %102 = or i1 %100, %101
  br i1 %102, label %if.then14, label %if.else14

if.then14:
  %103 = mul nsw i32 %i, 3
  %104 = add nsw i32 %i, 1
  %105 = mul nsw i32 %104, 5
  %106 = mul nsw i32 %103, 1
  %107 = sub nsw i32 %105, %106
  %108 = zext i32 %107 to i64
  %109 = zext i32 %i to i64
  %110 = icmp slt i64 %109, 16
  br i1 %110, label %if.then15, label %if.else15

if.then15:
  %111 = mul nsw i64 %108, 1
  %112 = sdiv i64 %111, 1