import com.eva.ro.contab.corelare.FisaCanalCalcul;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

public class A11Publicare {
    private static void verify(String label, Map<String, String> rules, long expected) {
        long result = FisaCanalCalcul.stocCalculat(List.of(new BigDecimal("13"),new BigDecimal("9")),new BigDecimal("5"), new BigDecimal("4"), 2, rules);
        if (result != expected) throw new AssertionError(label + " computed " + result);
        System.out.println(label+" expected "+expected+" observed "+result);
    }
    public static void main(String[] args) {
        verify("baseline 13+9-5-4-2",Map.of(),11);
        verify("enabled supplier 6 pieces",Map.of("EVA_T352_FURNIZOR_IN_OFERTA","Y","CANT_FURNIZOR","6"),11);
        verify("enabled supplier 40 percent",Map.of("EVA_T352_FURNIZOR_IN_OFERTA","Y","CANT_FURNIZOR","40%"),11);
        verify("disabled supplier",Map.of("EVA_T352_FURNIZOR_IN_OFERTA","N","CANT_FURNIZOR","6"),11);
        verify("real supported rule 50 percent",Map.of("EVA_StocProcent","50"),5);
    }
}
