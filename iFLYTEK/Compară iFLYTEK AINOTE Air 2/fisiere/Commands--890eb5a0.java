package ro.iflyresearch.glasses;
/** JSON command builders recovered from BleFrameBuilder. IDs are not GATT opcodes. */
public final class Commands {
    private Commands(){}
    public static final int SYSTEM_INFO=62001,VERSION=62002,BATTERY=62003;
    private static String base(int command,int operation,long business){
        if(operation<0||business<0)throw new IllegalArgumentException("Nonnegative IDs required");
        return "{\"opt\":"+command+",\"optNum\":"+operation+",\"biz_num\":"+business;
    }
    public static String query(int command,int operation,long business){
        if(command!=SYSTEM_INFO&&command!=VERSION&&command!=BATTERY)throw new IllegalArgumentException("Unsupported query");
        return base(command,operation,business)+"}";
    }
    public static String startRecording(int operation,long business,int mode,int compression,int multiMode){
        if(mode<1||mode>10||compression<0||multiMode<0)throw new IllegalArgumentException("Invalid record parameters");
        return base(62201,operation,business)+",\"translationScene\":"+mode+",\"multiModeSwitch\":"+multiMode+",\"compressionRatio\":"+compression+"}";
    }
    public static String stopRecording(int operation,long business,Integer mode){
        if(mode!=null&&(mode<1||mode>10))throw new IllegalArgumentException("Mode");
        return base(62202,operation,business)+(mode==null?"":",\"translationScene\":"+mode)+"}";
    }
}
