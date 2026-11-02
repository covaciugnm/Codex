package com.eva.ro.contab.form;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;
import com.eva.ro.contab.setup.EvaMetadata;
public class A11Job {
 public static void main(String[] args) throws Exception {
  if (args.length==1 && args[0].equals("column")) {
   int[][] cases={{10,40,10,40},{10,40,40,0},{10,40,41,0},{10,40,39,40},{11,10,5,0},{10,0,10,0},{10,40,0,0},{14,2000,255,2000}};
   for(int[] c:cases){
    List<Object[]> out=EvaMetadata.coloaneDeLargit(new Object[][]{{"COL",c[0],c[1],"x"}},n->c[2]);
    int got=out.isEmpty()?0:((Number)out.get(0)[1]).intValue();
    if(got!=c[3])throw new AssertionError(java.util.Arrays.toString(c)+":"+got);
    System.out.println(java.util.Arrays.toString(c)+" => "+got);
   }return;
  }
  String k=JobFundal.cheieBloc(11);boolean one=JobFundal.ocupaExclusiv(k,JobFundal.conflictBloc(11));
  boolean two=JobFundal.ocupaExclusiv(k,JobFundal.conflictBloc(11));
  System.out.println("ACQUIRE="+one+" SAME_OWNER_REENTRY="+two);System.out.flush();
  if(!one||two)throw new AssertionError();
  new BufferedReader(new InputStreamReader(System.in)).readLine();JobFundal.elibereaza(k);
  System.out.println("AFTER_RELEASE="+JobFundal.ocupaExclusiv(k,JobFundal.conflictBloc(11)));JobFundal.elibereaza(k);
 }
}
