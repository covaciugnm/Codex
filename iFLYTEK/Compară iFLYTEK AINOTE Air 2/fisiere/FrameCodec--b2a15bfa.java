package ro.iflyresearch.glasses;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

/** Reconstructed application frame format, not an official iFLYTEK SDK. */
public final class FrameCodec {
    private static final byte[] MAGIC={(byte)0xaa,(byte)0xff,0x55,0};
    private FrameCodec() {}
    public static int crc8(byte[] data, int length) {
        if(length<0||length>data.length)throw new IllegalArgumentException("CRC length");
        int crc=0;
        for(int i=0;i<length;i++) {crc^=data[i]&255;for(int bit=0;bit<8;bit++)crc=((crc&128)!=0?(crc<<1)^7:crc<<1)&255;}
        return crc;
    }
    public static byte[] json(int sequence,String json) {
        if(json==null)throw new NullPointerException("json");
        return encode(sequence,1,1,1,json.getBytes(StandardCharsets.UTF_8));
    }
    public static byte[] encode(int sequence,int channel,int payloadType,int subtype,byte[] payload) {
        if(sequence<0||sequence>65535||payload.length>65532)throw new IllegalArgumentException("16-bit frame limit");
        for(int v:new int[]{channel,payloadType,subtype})if(v<0||v>255)throw new IllegalArgumentException("byte range");
        byte[] out=new byte[payload.length+17];System.arraycopy(MAGIC,0,out,0,4);
        out[8]=1;out[9]=(byte)channel;put16(out,10,sequence);put16(out,12,payload.length+3);
        out[14]=(byte)payloadType;out[15]=(byte)subtype;System.arraycopy(payload,0,out,16,payload.length);
        out[out.length-1]=(byte)crc8(out,out.length-1);return out;
    }
    public static Frame decode(byte[] bytes) {
        if(bytes.length<17)throw new IllegalArgumentException("Truncated frame");
        for(int i=0;i<4;i++)if(bytes[i]!=MAGIC[i])throw new IllegalArgumentException("Frame magic");
        int size=u16(bytes,12);if(size<3||bytes.length!=14+size)throw new IllegalArgumentException("Frame length");
        if(crc8(bytes,bytes.length-1)!=(bytes[bytes.length-1]&255))throw new IllegalArgumentException("CRC mismatch");
        return new Frame(bytes[8]&255,bytes[9]&255,u16(bytes,10),bytes[14]&255,bytes[15]&255,Arrays.copyOfRange(bytes,16,bytes.length-1));
    }
    private static void put16(byte[] a,int o,int n){a[o]=(byte)n;a[o+1]=(byte)(n>>>8);}
    private static int u16(byte[] a,int o){return (a[o]&255)|((a[o+1]&255)<<8);}
    public static final class Frame {
        public final int version,channel,sequence,payloadType,subtype;
        private final byte[] payload;
        Frame(int v,int c,int s,int p,int t,byte[] b){version=v;channel=c;sequence=s;payloadType=p;subtype=t;payload=b;}
        public byte[] payload(){return payload.clone();}
        public String json(){if(payloadType!=1)throw new IllegalStateException("Not JSON payload");return new String(payload,StandardCharsets.UTF_8);}
    }
    /** Accepts fragmentation/coalescing. On invalid data, clears state and throws; caller may reconnect. */
    public static final class Assembler {
        private final ByteArrayOutputStream pending=new ByteArrayOutputStream();
        private int expected=-1;
        public synchronized List<Frame> accept(byte[] chunk) {
            List<Frame> frames=new ArrayList<>();
            try {for(byte b:chunk){
                pending.write(b);int n=pending.size();
                if(n<=4&&b!=MAGIC[n-1])throw new IllegalArgumentException("Stream magic");
                if(n==14){byte[] header=pending.toByteArray();int size=u16(header,12);if(size<3)throw new IllegalArgumentException("Stream length");expected=14+size;}
                if(n==expected){frames.add(decode(pending.toByteArray()));reset();}
            }}catch(RuntimeException e){reset();throw e;}return frames;
        }
        public synchronized void reset(){pending.reset();expected=-1;}
        public synchronized int pendingBytes(){return pending.size();}
    }
}
