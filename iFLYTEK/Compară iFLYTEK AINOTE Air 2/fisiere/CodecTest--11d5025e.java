import ro.iflyresearch.glasses.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
public class CodecTest {
 static int checks=0;
 static void check(boolean b){checks++;if(!b)throw new AssertionError("Check "+checks);}
 static void rejects(Runnable r){boolean rejected=false;try{r.run();}catch(IllegalArgumentException e){rejected=true;}check(rejected);}
 public static void main(String[] args){
  byte[] known="123456789".getBytes(StandardCharsets.US_ASCII);check(FrameCodec.crc8(known,9)==0xf4);
  byte[] wire=FrameCodec.json(0x1234,"{}");
  byte[] header={(byte)0xaa,(byte)0xff,0x55,0,0,0,0,0,1,1,0x34,0x12,5,0,1,1,0x7b,0x7d};
  check(Arrays.equals(header,Arrays.copyOf(wire,18)));check(wire.length==19);
  FrameCodec.Frame parsed=FrameCodec.decode(wire);check(parsed.sequence==0x1234);check(parsed.json().equals("{}"));
  for(int cut=0;cut<=wire.length;cut++){
   FrameCodec.Assembler a=new FrameCodec.Assembler();List<FrameCodec.Frame> frames=new ArrayList<>();
   frames.addAll(a.accept(Arrays.copyOfRange(wire,0,cut)));frames.addAll(a.accept(Arrays.copyOfRange(wire,cut,wire.length)));
   check(frames.size()==1&&a.pendingBytes()==0&&frames.get(0).json().equals("{}"));
  }
  FrameCodec.Assembler a=new FrameCodec.Assembler();byte[] two=new byte[wire.length*2];System.arraycopy(wire,0,two,0,wire.length);System.arraycopy(wire,0,two,wire.length,wire.length);check(a.accept(two).size()==2);
  byte[] corrupt=wire.clone();corrupt[16]^=1;rejects(()->FrameCodec.decode(corrupt));rejects(()->a.accept(corrupt));check(a.pendingBytes()==0);check(a.accept(wire).size()==1);
  rejects(()->FrameCodec.decode(Arrays.copyOf(wire,wire.length-1)));rejects(()->FrameCodec.json(-1,"{}"));rejects(()->FrameCodec.encode(0,1,1,1,new byte[65533]));
  byte[] max=FrameCodec.encode(65535,1,2,1,new byte[65532]);check(FrameCodec.decode(max).payload().length==65532);
  check(Commands.query(62003,1,0).equals("{\"opt\":62003,\"optNum\":1,\"biz_num\":0}"));
  check(Commands.startRecording(2,1,2,0,0).contains("\"translationScene\":2"));rejects(()->Commands.query(123,1,0));
  check(Commands.stopRecording(3,1,null).equals("{\"opt\":62202,\"optNum\":3,\"biz_num\":1}"));
  check(Commands.stopRecording(3,1,2).endsWith("\"translationScene\":2}"));
  rejects(()->Commands.stopRecording(3,1,11));
  System.out.println("PASS "+checks+" codec/command checks; hardware not exercised");
 }
}
