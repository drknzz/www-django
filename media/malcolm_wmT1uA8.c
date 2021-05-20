/*@ ensures \result == 2.; */

double malcolm1() {
  double A, B;
  A=2.0;
  /*@ ghost int i = 1; */

  /*@ loop invariant A== \pow(2.,i) && 
    @          1 <= i <= 53;
    @ loop variant (53-i); */

  while (A != (A+1)) {
    A*=2.0;
    /*@ ghost i++; */
  }

  /*@ assert i==53 && A== 0x1.p53; */

  B=1;
  /*@ ghost i = 1;*/ 

 /*@ loop invariant B == i && (i==1 || i == 2);
   @ loop variant (2-i); */
  
  while ((A+B)-A != B) {
    B++;
    /*@ ghost i++; */
  }

  return B;

}
