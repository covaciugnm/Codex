import ro.iflyresearch.glasses.*;
public class BatteryQuery {
 public static void main(String[] args){
  String json=Commands.query(Commands.BATTERY,1,0);
  byte[] packet=FrameCodec.json(0,json);
  System.out.println("Service: "+GlassesProfile.SERVICE);
  System.out.println("Write: "+GlassesProfile.COMMAND_WRITE);
  System.out.println("Subscribe: "+GlassesProfile.NOTIFY);
  System.out.println(json);
  for(byte b:packet)System.out.printf("%02x",b&255);
  System.out.println("\nPacket generated only; not sent to hardware.");
 }
}
