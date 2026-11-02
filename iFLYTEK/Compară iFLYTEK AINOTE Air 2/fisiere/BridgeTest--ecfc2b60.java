import ro.iflyresearch.glasses.RecorderBridge;
import com.iflytek.easytrans.headset.bluetooth.recorder.Mode;
import com.alipay.verifyiotidentity.obfuscated.*;
public class BridgeTest {
 public static class FakeRecorder {
  public kh4 callback;public boolean started,stopped,released,original,translated;
  public void j(kh4 value){callback=value;}
  public void m(String s,Mode m,int c,int multi){started=true;callback.onStart(s,m);callback.onData(s,m,new yw());}
  public void stop(String s){stopped=true;}
  public void release(){released=true;}
  public void setOriginalEnable(String s,boolean e){original=e;}
  public void setTranslateEnable(String s,boolean e){translated=e;}
 }
 public static void main(String[] args)throws Exception {
  FakeRecorder fake=new FakeRecorder();int[] calls={0};
  RecorderBridge b=new RecorderBridge(fake,(s,t,pcm,opus)->{if(!s.equals("test")||t!=2||pcm[0]!=1||opus!=null)throw new AssertionError();calls[0]++;});
  b.start("test",2,0,0);b.originalAudio("test",true);b.translatedAudio("test",true);b.stop("test");b.close();b.close();
  if(calls[0]!=1||!fake.started||!fake.stopped||!fake.released||!fake.original||!fake.translated)throw new AssertionError();
  try{b.stop("test");throw new AssertionError();}catch(IllegalStateException expected){}
  System.out.println("PASS recorder bridge ABI simulation; vendor runtime and hardware not exercised");
 }
}
