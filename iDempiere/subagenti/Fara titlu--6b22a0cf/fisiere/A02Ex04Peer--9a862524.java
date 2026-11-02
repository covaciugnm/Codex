package com.eva.ro.contab.corelare;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.sql.Timestamp;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;
public final class A02Ex04Peer {
 public static void main(String[] a)throws Exception{
  Path cases=Path.of(a[0]); var payload=new AtomicReference<String>();var requested=new AtomicReference<String>();
  HttpServer srv=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
  srv.createContext("/api/ext/v1/orders",ex->{requested.set(ex.getRequestMethod()+" "+ex.getRequestURI().getRawPath()+"?"+ex.getRequestURI().getRawQuery());var body=payload.get().getBytes(StandardCharsets.UTF_8);ex.getResponseHeaders().set("Content-Type","application/json");ex.sendResponseHeaders(200,body.length);try(var stream=ex.getResponseBody()){stream.write(body);}});srv.start();
  try{
   var config=new SursaSiteConfig.Config("http://127.0.0.1:"+srv.getAddress().getPort()+"/api/ext/v1","peer-synthetic-key","canal-a",List.of(),List.of(),null);var adapter=SursaCesiro1.deschide(config);
   for(String label:new String[]{"consistent_three","legitimate_empty","inconsistent_empty","inconsistent_subset","missing_items","malformed"}){
    payload.set(Files.readString(cases.resolve(label+".json")));
    try{var orders=adapter.comenzi(Timestamp.valueOf("2026-11-02 00:00:00"),Timestamp.valueOf("2026-11-03 00:00:00"),null);
      System.out.println("CASE|"+label+"|OK|"+orders.size()+"|"+orders.stream().map(x->String.valueOf(x.id())).toList()+"|"+requested.get());
      if(label.equals("consistent_three")){var item=orders.get(0);Timestamp newer=Timestamp.from(item.actualizat().toInstant().plusSeconds(60));System.out.println("VERSION|equal|"+PreiaDinSite.deActualizat(item,item.actualizat()));System.out.println("VERSION|sourceOlderThanPersisted|"+PreiaDinSite.deActualizat(item,newer));}
    }catch(Exception e){System.out.println("CASE|"+label+"|ERROR|"+e.getClass().getSimpleName()+"|"+requested.get());}
   }
  }finally{srv.stop(0);}
 }
}
