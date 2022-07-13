# SM4-SBox-CompositeField
AES 和 SM4 的 S 盒生成都是基于GF(2<sup>8</sup>)进行构造的，利用逆运算和仿射变换。仿射变换本身就能表示成逻辑运算，故重点关注求逆运算。      
AES 和 SM4 的表达都是基于多项式基，以 AES 的有限域为例，假设A为多项式x<sup>8</sup>+x<sup>4</sup>+x<sup>3</sup>+x+1的根，即A<sup>8</sup>+A<sup>4</sup>+A<sup>3</sup>+A+1=0,那么任何一个元素x可以表示为x=x<sub>7</sub>A<sup>7</sup>+x<sub>6</sub>A<sup>6</sup>+x<sub>5</sub>A<sup>5</sup>+x<sub>4</sub>A<sup>4</sup>+x<sub>3</sub>A<sup>3</sup>+x<sub>2</sub>A<sup>2</sup>+x<sub>1</sub>A+x<sub>0</sub>。
这种做法是将GF(2<sup>8</sup>)直接看作GF(2)的8次扩域。我们也可以不这么看，将GF(2<sup>8</sup>)看成GF(2<sup>4</sup>)的2次扩域，GF(2<sup>4</sup>)可以进一步看作GF(2<sup>2</sup>)的2次扩域，再进一步GF(2<sup>2</sup>)可以看作GF(2)的2次扩域。而GF(2<sup>8</sup>)的求逆运算，可以通过数学表达式，转换为GF(2<sup>4</sup>)的求逆和一些乘、加操作。这些操作可以进一步向下转化。    
从而实现对AES和SM4的bit直接进行逻辑运算，避免查表操作，同时结合AESNI指令集可以将SM4的S盒运算转化为AES的S盒运算。
