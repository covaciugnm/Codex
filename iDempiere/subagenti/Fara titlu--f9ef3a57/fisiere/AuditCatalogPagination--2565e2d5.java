import java.io.IOException;
import java.net.*;
import java.nio.file.*;

public final class AuditCatalogPagination {
    @FunctionalInterface interface Operation { void run() throws Exception; }
    static int passed=0;
    static void deny(String name, Operation operation) throws Exception {
        try { operation.run(); throw new AssertionError("CANARY_ALLOWED:"+name); }
        catch (SecurityException expected) {
            passed++;
            System.out.println("CANARY|"+name+"|DENIED|"+expected.getClass().getName()+"|"+expected.getMessage());
        }
    }
    @SuppressWarnings("removal")
    public static void main(String[] args) throws Exception {
        Path lab=Path.of(args[0]).toAbsolutePath().normalize();
        if(System.getSecurityManager()==null) throw new AssertionError("SecurityManager missing");
        String marker=Files.readString(lab.resolve("fixture/canary.txt"));
        if(!marker.equals("A08_SYNTHETIC_ONLY"))throw new AssertionError("read fixture marker");
        passed++;System.out.println("CANARY|fixture_read|ALLOWED");
        deny("write_lab",()->Files.writeString(lab.resolve("fixture/forbidden.txt"),"NO"));
        deny("read_outside",()->Files.readString(Path.of("D:/CodexWork/forbidden-outside-a08.txt")));
        deny("tcp_loopback",()->{try(Socket s=new Socket()){s.connect(new InetSocketAddress("127.0.0.1",9),100);}});
        deny("tcp_remote",()->{try(Socket s=new Socket()){s.connect(new InetSocketAddress("203.0.113.1",9),100);}});
        deny("listen",()->{try(ServerSocket s=new ServerSocket(0)){} });
        deny("udp",()->{try(DatagramSocket s=new DatagramSocket(0)){} });
        deny("exec",()->new ProcessBuilder("cmd.exe","/c","exit","0").start());
        deny("remove_security_manager",()->System.setSecurityManager(null));
        if(passed!=9)throw new AssertionError("9 canaries required");
        System.out.println("CANARIES_COMPLETE|9");
        // Product class is resolved only after all runtime canaries have completed.
        Class.forName("CatalogProductProbe").getMethod("run",String.class).invoke(null,lab.toString());
    }
}
