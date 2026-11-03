import java.math.BigDecimal;
import java.lang.reflect.Field;
import java.security.Permission;
import java.util.Properties;
import org.eevolution.model.MPPProductBOMLine;

/** Audit-only witness. It never saves a PO or connects to any database. */
public class A05NativeBomBoundary {
    static int networkDenied;
    static class NoNetwork extends SecurityManager {
        public void checkPermission(Permission p) {}
        public void checkConnect(String host, int port) { networkDenied++; throw new SecurityException("audit denies all network"); }
        public void checkListen(int port) { throw new SecurityException("audit denies listening"); }
    }
    static class LineFields extends MPPProductBOMLine {
        boolean coproduct;
        BigDecimal quantity;
        LineFields() { super(new Properties(),0,"audit-uninitialized"); }
        @Override public boolean isCoProduct() { return coproduct; }
        @Override public BigDecimal getQty(boolean scrap) { return quantity; }
        @Override public BigDecimal getQtyBOM() { return quantity; }
        @Override public int getLine() { return 10; }
        boolean nativeBeforeSave() { return super.beforeSave(false); }
    }
    public static void main(String[] args) throws Exception {
        System.setSecurityManager(new NoNetwork());
        try {
            new MPPProductBOMLine(new Properties(),0,"audit-standalone");
            System.out.println("constructor|SUCCESS_NO_SAVE");
        } catch(Throwable e) {
            Throwable cause=e;
            while(cause.getCause()!=null) cause=cause.getCause();
            System.out.println("constructor|BLOCKED|"+e.getClass().getName()+"|"+cause.getClass().getName());
            for(StackTraceElement frame:cause.getStackTrace()) {
                if(frame.getClassName().startsWith("org.")) System.out.println("init_frame|"+frame);
            }
        }
        // Native model initialization may leave class initialization in failure.
        // The narrow method test is run only if this runtime can create its subclass.
        try {
            Field f=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");f.setAccessible(true);
            sun.misc.Unsafe unsafe=(sun.misc.Unsafe)f.get(null);
            LineFields line=(LineFields)unsafe.allocateInstance(LineFields.class);
            for(int qty:new int[]{2,3}) {
                line.coproduct=false;line.quantity=BigDecimal.valueOf(qty);
                if(!line.nativeBeforeSave()) throw new AssertionError("native component should permit regular positive QtyBOM");
                System.out.println("native_before_save|regular_qty_"+qty+"|ALLOWED");
            }
            line.coproduct=true;line.quantity=BigDecimal.ONE;
            try { line.nativeBeforeSave();throw new AssertionError("positive coproduct was expected to be rejected"); }
            catch(org.adempiere.exceptions.AdempiereException expected) {System.out.println("native_before_save|positive_coproduct|REJECTED");}
            line.quantity=BigDecimal.ONE.negate();
            if(!line.nativeBeforeSave()) throw new AssertionError("negative coproduct rejected");
            System.out.println("native_before_save|negative_coproduct|ALLOWED");
        } catch(NoClassDefFoundError | ExceptionInInitializerError e) {
            System.out.println("component_boundary|UNAVAILABLE|"+e.getClass().getName());
        }
        System.out.println("network_denied|"+networkDenied);
        System.out.println("persistent_PO_effect|NONE");
    }
}
