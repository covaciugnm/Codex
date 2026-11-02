package ro.iflyresearch.glasses;
import java.util.UUID;
public final class GlassesProfile {
    private GlassesProfile(){}
    public static final String APK_SHA256="73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2";
    public static final UUID SERVICE=UUID.fromString("434f544f-5250-5050-414b-4554594c4669");
    public static final UUID COMMAND_WRITE=UUID.fromString("00006001-0000-1000-8000-00805f9b34fb");
    public static final UUID NOTIFY=UUID.fromString("00006002-0000-1000-8000-00805f9b34fb");
    public static final UUID AUDIO_WRITE=NOTIFY;
    public static final int PCM_SAMPLE_RATE=16000;
    public static final int PCM_BITS=16;
    public static final int AUDIO_GLASS_SELF=5,AUDIO_GLASS_OTHER=6;
    public static final int MODE_DIALOG=1,MODE_LIVE_LISTENING=2;
}
