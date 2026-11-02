package com.eva.ro.contab.corelare;
import java.util.*;
import java.math.*;
import com.eva.ro.contab.documente.Etichete;
public class CashMatrix {
 static BigDecimal d(int q){return BigDecimal.valueOf(q);}
 static List<AplicareDecont.LinieD> lines(int[] vals,int[] costs){
  var all=new ArrayList<AplicareDecont.LinieD>();
  for(int i=0;i<vals.length;i++){
   var cod=d(vals[i]);var remit=cod.subtract(d(costs[i]));var res=MotorCorelare.evalueazaDecontare(cod,remit,null,d(costs[i]),"RON","RON");
   all.add(new AplicareDecont.LinieD(20+i,cod,remit,null,res.diferenta(),res.cauza(),"LEGAT_AUTO",510+i));
  }return all;
 }
 public static void main(String[] args){
  Etichete.limba(()->"ro");int[] expected={31,57,73};int[] costs={3,5,4};int[] order={0,1,2};
  int used=0;
  for(int i:order)for(int j:order)for(int k:order){
   if(i==j||i==k||j==k)continue;
   int[] vals={expected[i],expected[j],expected[k]};int abs=0;for(int n=0;n<3;n++)abs+=Math.abs(expected[n]-vals[n]);
   var l=lines(vals,costs);String gate=AplicareDecont.poarta(d(149),"TRANSIT",false,List.of("TRANSIT"),d(149),l,true);
   System.out.println("perm="+i+j+k+" absolute_disparity="+abs+" total_net=149 gate="+(gate==null?"ALLOW":"BLOCK"));
   if(gate!=null)throw new AssertionError("sum-equivalence not reproduced");used++;
   if(AplicareDecont.poarta(d(149),"TRANSIT",true,List.of("TRANSIT"),d(149),l,true)==null)throw new AssertionError("repeat should close");
   if(AplicareDecont.poarta(d(149),"TRANSIT",false,List.of("TRANSIT"),d(150),l,true)==null)throw new AssertionError("different bank amount");
  }if(used!=6)throw new AssertionError();
 }
}
