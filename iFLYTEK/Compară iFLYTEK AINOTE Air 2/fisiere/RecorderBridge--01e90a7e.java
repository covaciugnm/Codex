package ro.iflyresearch.glasses;

import java.lang.reflect.*;
import java.util.Objects;

/** Adapter for an already initialized vendor recorder IN THE SAME PROCESS/classloader.
 * Does not load an APK, bypass sandboxing, or establish a Bluetooth session.
 */
public final class RecorderBridge implements AutoCloseable {
    public interface Listener {
        void onAudio(String session,int type,byte[] pcm16le,byte[] opus);
        default void onEvent(String event,Object[] args){}
    }
    private final Object recorder;
    private final Class<?> modeType,callbackType;
    private final Object callback;
    private final Listener listener;
    private boolean closed;
    public RecorderBridge(Object recorder,Listener listener) throws ReflectiveOperationException {
        this.recorder=Objects.requireNonNull(recorder);this.listener=Objects.requireNonNull(listener);
        ClassLoader loader=recorder.getClass().getClassLoader();
        modeType=Class.forName("com.iflytek.easytrans.headset.bluetooth.recorder.Mode",false,loader);
        callbackType=Class.forName("com.alipay.verifyiotidentity.obfuscated.kh4",false,loader);
        // Verify the known ABI before registering a callback.
        recorder.getClass().getMethod("m",String.class,modeType,int.class,int.class);
        recorder.getClass().getMethod("stop",String.class);
        Class<?> audio=Class.forName("com.alipay.verifyiotidentity.obfuscated.yw",false,loader);
        audio.getMethod("e");audio.getMethod("f");
        callback=Proxy.newProxyInstance(loader,new Class<?>[]{callbackType},(proxy,method,args)->{
            if(method.getDeclaringClass()==Object.class){
                if(method.getName().equals("hashCode"))return System.identityHashCode(proxy);
                if(method.getName().equals("equals"))return proxy==args[0];
                return "ExperimentalRecorderCallback";
            }
            if(method.getName().equals("onData")) {
                int type=(Integer)args[1].getClass().getMethod("getValue").invoke(args[1]);
                byte[] pcm=(byte[])audio.getMethod("e").invoke(args[2]);
                byte[] opus=(byte[])audio.getMethod("f").invoke(args[2]);
                listener.onAudio((String)args[0],type,pcm.clone(),opus==null?null:opus.clone());
            }else listener.onEvent(method.getName(),args==null?new Object[0]:args.clone());
            return null;
        });
        call("j",new Class<?>[]{callbackType},callback);
    }
    private Object mode(int code) throws ReflectiveOperationException {
        Object[] values=(Object[])modeType.getMethod("values").invoke(null);
        for(Object v:values)if(((Integer)modeType.getMethod("getValue").invoke(v))==code)return v;
        throw new IllegalArgumentException("Unknown mode "+code);
    }
    private void call(String method,Class<?>[] types,Object... args) throws ReflectiveOperationException {
        if(closed)throw new IllegalStateException("Closed recorder bridge");
        try{recorder.getClass().getMethod(method,types).invoke(recorder,args);}
        catch(InvocationTargetException e){throw new ReflectiveOperationException("Vendor call failed: "+method,e.getCause());}
    }
    public void start(String session,int mode,int compression,int multiMode) throws ReflectiveOperationException {
        if(session==null||session.isEmpty()||compression<0||multiMode<0)throw new IllegalArgumentException("Recording parameters");
        call("m",new Class<?>[]{String.class,modeType,int.class,int.class},session,mode(mode),compression,multiMode);
    }
    public void stop(String session) throws ReflectiveOperationException {call("stop",new Class<?>[]{String.class},session);}
    public void originalAudio(String session,boolean enable) throws ReflectiveOperationException {call("setOriginalEnable",new Class<?>[]{String.class,boolean.class},session,enable);}
    public void translatedAudio(String session,boolean enable) throws ReflectiveOperationException {call("setTranslateEnable",new Class<?>[]{String.class,boolean.class},session,enable);}
    public void close() throws ReflectiveOperationException {if(!closed){call("release",new Class<?>[0]);closed=true;}}
}
