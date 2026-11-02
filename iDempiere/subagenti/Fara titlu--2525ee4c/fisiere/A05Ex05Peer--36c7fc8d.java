package com.eva.ro.contab.corelare;

import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Set;
import com.eva.ro.contab.documente.JsonMic;

public class A05Ex05Peer {
    public static void main(String[] args) throws Exception {
        String wire = Files.readString(Path.of(args[0]));
        Object obj = JsonMic.citeste(wire);
        DetaliuComanda parsed = DetaliuComanda.din(wire);
        AdaptorPlatforma.Detaliu staging = SursaCesiro1.detaliu(obj, List.of());
        System.out.println("STAGING_DETAIL|" + staging.facturi().size() + "|" + staging.expedieri().size());
        for (DetaliuComanda.Linie line : parsed.linii())
            System.out.println("NATIVE_DETAIL|" + line.pozitie() + "|" + line.sku() + "|" + line.cantitate()
                + "|" + line.cotaTva() + "|" + line.totalLinie());
        System.out.println("TOTAL|" + parsed.totalRon() + "|SELLER_PRESENT|" + (parsed.cuiVanzator() != null && !parsed.cuiVanzator().isBlank()));
        var z = BigDecimal.ZERO;
        var ctx = new ValidareComanda.Context("123456", Set.of(), Map.of("cod","RAMBURS"), Set.of(),
            Set.of(), Map.of("individual","PF"), true,true,21,Set.of(21),true,z,true,true,true,true,
            null,null,Set.of(),z,false,false);
        for (boolean own : List.of(false,true)) {
            var c = new ValidareComanda.Comanda(own,"123456","new","cod",null,false,"human","RON",
                List.of(),z,z,z,z,"individual",true,true,null,List.of());
            var verdict = ValidareComanda.valideaza(c, ctx, true);
            System.out.println("STUB_VALIDATOR|" + own + "|" + verdict.stare() + "|" + verdict.motiveText() + "|ELIGIBLE_LINES=" + verdict.val().size());
        }
    }
}
